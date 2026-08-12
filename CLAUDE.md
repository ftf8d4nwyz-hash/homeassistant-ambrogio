# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Home Assistant custom integration (HACS, `custom_components/ambrogio_robot`) for Ambrogio /
Zucchetti Centro Sistemi robot lawn mowers. It is a cloud-polling integration, UI-configured only —
there is no YAML setup path (`async_setup` returns `True` and does nothing).

The repo started from [integration_blueprint](https://github.com/ludeeus/integration_blueprint); some
scaffolding comments and names still reference the blueprint. The README states the integration is
still in development, and that is accurate — see "Work in progress" below before assuming code is live.

## Commands

Python 3.11. Dev deps are **not** the runtime deps — `requirements_dev.txt` adds
`pytest-homeassistant-custom-component`, which pulls in `pytest` and the HA test helpers.

```bash
pip install -r requirements_dev.txt        # test/dev environment
pip install -r requirements.txt            # run-a-real-HA environment

scripts/lint                               # ruff check . --fix
python3 -m ruff check .                    # what CI runs (no --fix)

pytest tests/                              # full suite (pytest config lives in setup.cfg)
pytest tests/test_init.py -k test_setup_and_reload    # single test
pytest --cov-report term-missing --cov=custom_components.ambrogio_robot tests

scripts/develop                            # hass -c . --debug, serves on :8123
```

`scripts/develop` runs Home Assistant against the repo root as its config dir, so it needs a
`configuration.yaml` — `scripts/setup` copies `configuration-template.yaml` into place. The
devcontainer picks dev vs run deps from the `BUILD_TYPE` env var set in `.devcontainer.json`
(copy from `.devcontainer-template.json`).

CI (`.github/workflows/`) runs ruff, hassfest, HACS validation, and pytest with `--timeout=9 -n auto`
— tests must not rely on real network or on sleeping longer than 9s.

Releases are cut with `bumpver`; it rewrites the version in three places at once (`setup.cfg`,
`manifest.json`, `const.py: VERSION`) and commits, tags, and pushes. Don't hand-edit those versions.

## Architecture

### Two unrelated APIs

Authentication and data come from different backends, which is the main thing to internalize:

- `api/firebase.py` — **discovery/auth only.** Signs in against Google Identity Toolkit
  (`identitytoolkit.googleapis.com`) with email/password, then opens a **websocket** to the
  Ambrogio Firebase DB to list the robots in the user's "garage". Returns tokens plus an
  `imei -> name` map. Raises `AmbrogioRobotException`.
- `api/api.py` — **all robot data and commands.** A Telit deviceWISE **TR50** JSON-RPC client
  (`api-de.devicewise.com/api`), ported from the deviceWISE Python sample. Stateful: `execute()`
  posts a command, `get_response()` returns the parsed result of the *last* call, and a session id is
  refreshed transparently when the API reports an invalid session. Errors are
  `AmbrogioRobotApiClient{,Communication,Authentication}Error`.

### Coordinator

`AmbrogioDataUpdateCoordinator` (`coordinator.py`) is where nearly all the logic lives. Its `data` is a
`dict[imei, dict]` seeded with every attribute key up front, so entities can read attributes before the
first poll without `KeyError`.

- One `thing.list` call per refresh fetches all mowers; `async_update_mower()` maps the raw payload
  onto the flat per-mower dict (state name + icon from the `ROBOT_STATES` list indexed by the numeric
  state, model derived from the first 6 chars of the serial via `ROBOT_MODELS`, error text via
  `ROBOT_ERRORS`).
- The poll interval is **dynamic**: `UPDATE_INTERVAL_DEFAULT` (300s) normally, `UPDATE_INTERVAL_WORKING`
  (60s) when any mower is working.
- Mowers sleep. Every command goes through `async_prepare_for_command()`, which reuses a
  <10s-old connection state, otherwise sends a wake-up and polls `thing.find` up to 6 times at 5s
  intervals. Wake-up is an **SMS** (`sms.send` with body `UP`), not an API method.
- Each command method (`async_work_now`, `async_charge_until`, `async_keep_out`, …) is a thin
  `method.exec` wrapper. Note the off-by-one conversions to the device's 0-based indexing:
  profile, area, and weekday are all decremented, with area `255` meaning "no area".

### Entities

`AmbrogioRobotEntity` (`entity.py`) is a `CoordinatorEntity` subclass shared by all platforms. It
reads through `self._get_attribute(key)` into the coordinator's per-mower dict, sets
`unique_id = slugify(f"{imei}_{key}")`, and forces `entity_id` to `{platform}.{unique_id}`. Device
identity is the IMEI, so all of a mower's entities group under one device.

Every platform module (`sensor`, `binary_sensor`, `device_tracker`, `vacuum`) has the same shape: a
module-level `ENTITY_DESCRIPTIONS` tuple, and an `async_setup_entry` that builds the cross-product of
`coordinator.robots` × `ENTITY_DESCRIPTIONS`. Subclasses override only the value properties.

### Services

Service names and their voluptuous schemas are declared in `const.py`
(`SERVICE_*` / `SERVICE_*_SCHEMA`), user-facing metadata in `services.yaml`, and dispatch in
`services.py` — a single `async_handle_service` handler resolves the caller's `device_id`s to
coordinators via the device registry, then branches to a private `_async_*` function per service.

### Config flow

`config_flow.py` offers three entry paths: `user_pass` (Firebase email/password), `oauth`
(Google/Apple, implemented as an HA *external step* that serves
`frontend/firebase_auth.html` as a static path and catches the redirect with
`AmbrogioAuthorizationCallbackView`), and `manual` (currently returns a `not_implemented` error).

## Adding an entity

Touching one file is never enough. In order:

1. Ensure the coordinator actually populates the attribute — add the key to the seed dict in
   `__init__` **and** set it in `async_update_mower()`.
2. Add an `ATTR_*` constant in `const.py`.
3. Add an entry to the platform's `ENTITY_DESCRIPTIONS` with a `translation_key`.
4. Add that `translation_key` under `entity.<platform>.<key>` in `translations/en.json`
   (and `strings.json`, which must stay in sync — hassfest validates it).
5. Add a test using a fixture (see below).

## Tests

`tests/conftest.py` stands up a real `aiohttp` test server (the `google_api` fixture) that impersonates
both the Google auth endpoint and the Firebase websocket, replaying canned frames from
`tests/fixtures/api_firebase/`. Fixtures are loaded by folder + filename via the local
`load_fixture(folder, filename)` helper — **not** HA's global `load_fixture`. Coordinator tests instead
patch `_async_update_data` with `tests/fixtures/controller/default_data.json`.

Custom integrations only load in tests because of the autouse `auto_enable_custom_integrations`
fixture; keep it.

## Work in progress — read before editing

Several things in the tree look wired up but are not:

- `__init__.py` exports **two** setup functions. The live `async_setup_entry` is blueprint OAuth2
  scaffolding that forwards platforms *without ever creating a coordinator* (so `hass.data[DOMAIN]`
  is never filled and every platform's `async_setup_entry` would `KeyError`). The real wiring —
  Firebase auth, robot list, coordinator, reload listener — is in `async_setup_entry2`, which nothing
  calls. Assume the intent is that `2` becomes the real one.
- `async_setup_services()` is never called, so no service is registered at runtime despite
  `services.py` / `services.yaml` / the schemas in `const.py` being complete.
- `tests/conftest.py` and `tests/test_init.py` patch `custom_components.ambrogio_robot.api_firebase.…`,
  but that module does not exist — the package layout is `api/firebase.py`, i.e.
  `custom_components.ambrogio_robot.api.firebase`. Those patch targets need updating before the
  affected tests can pass.
- There is no `diagnostics.py`; `tests/test_diagnostics.py` is an empty placeholder.
- In `async_update_mower`, `ATTR_WORKING` is computed by comparing the numeric state against
  `ROBOT_WORKING_STATES` (a list of ints), but the later "is it working" checks compare
  `mower[ATTR_STATE]`, which by then holds the state *name* string, against the same int list.

## Conventions

- Ruff config (`.ruff.toml`) mirrors Home Assistant core: docstrings required on every module,
  class, and function (`D`); no `print` (`T20`); `UP` pyupgrade rules. `CONTRIBUTING.md` also asks for
  black formatting.
- Constants belong in `const.py` — it holds the full model, state, and error tables. Prefer extending
  those tables over inlining literals.
- Upstream (`sHedC/homeassistant-ambrogio`) develops on `dev` and merges to `main`; PRs there are
  taken from `main`.
