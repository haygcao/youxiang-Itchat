# Changelog

## Unreleased

### Changed

- Refactored coupon scheduler registration into declarative platform metadata, reducing duplicated Taobao, JD, Pinduoduo, and Suning cron setup code.
- Added lazy imports for scheduler dependencies and platform API clients so modules can be imported without requiring the full runtime environment.
- Split shared coupon delivery helpers into `coupon.delivery` for chatroom lookup, text sending, image sending, and temporary image cleanup.
- Split common pricing helpers into `coupon.pricing`.
- Reworked Taobao and Pinduoduo coupon flows into smaller functions for material selection, message formatting, promotion URL handling, and delivery.
- Updated `main.py` to use explicit `run` import instead of wildcard imports.
- Added `.gitignore` for Python caches, virtual environments, logs, and local tooling noise.

### Fixed

- Fixed Pinduoduo retry call using the wrong argument count.
- Replaced unbounded recursive retries with bounded retry handling.
- Prevented negative Pinduoduo coupon prices when discounts exceed base price.
- Made Taobao token extraction tolerate multiple currency marker variants.
- Fixed Taobao non-coupon items using the wrong URL source for token generation.
- Avoided duplicate image deletion in Taobao flow.
- Prevented sending `@img@None` when image downloads fail.
- Fixed JD and Suning image cleanup by routing image delivery through the shared delivery helper.
- Made downloaded coupon images use a temporary directory with safer unique filenames instead of writing into the project root.
- Fixed `untils.common.__all__` containing an empty export name.
- Made config access fail clearly when `config.init()` has not run.

### Dependencies

- Added explicit `PyYAML` and `requests` runtime dependencies used by the project.
