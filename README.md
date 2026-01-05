# HA No Service

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

A Home Assistant custom integration that provides creative rejection reasons via the [no-as-a-service API](https://github.com/hotheadhacker/no-as-a-service).

Perfect for when you need a creative excuse to say "no" - now integrated into your Home Assistant!

## Features

- 🎲 **Random Rejection Reasons**: Access to 1,000+ pre-written creative excuses
- 🔄 **Auto-Update**: Sensor automatically refreshes every hour
- 🎯 **Manual Refresh**: Service call to get a new reason on demand
- 📊 **Sensor Integration**: Full Home Assistant sensor with attributes

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/Diondk/ha_no_service`
6. Select category: "Integration"
7. Click "Add"
8. Search for "HA No Service" and install

### Manual Installation

1. Download the latest release from the [releases page][releases]
2. Copy the `custom_components/ha_no_service` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

All configuration is done via the **Home Assistant UI**:

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for **HA No Service**
4. Enter your API URL:
   - Default/Public API: `https://naas.isalman.dev/no`
   - Custom: Use your own [no-as-a-service Docker instance](https://github.com/hotheadhacker/no-as-a-service) (e.g., `http://localhost:8080/no`)
5. Click **Submit**

The integration will automatically create a sensor and start fetching rejection reasons.

### Changing Configuration

To change the API URL:
- Go to **Settings → Devices & Services → HA No Service**
- Click the three dots (⋮) and select **Configure**
- Update the API URL
- Click **Submit**

### Legacy YAML Configuration (Deprecated)

**Note**: YAML configuration is deprecated and will be automatically migrated to the UI when Home Assistant restarts.

If you have existing YAML configuration like this:
```yaml
sensor:
  - platform: ha_no_service
    api_url: "https://naas.isalman.dev/no"
```

It will be automatically imported to the UI configuration. You can then remove it from your YAML files.

## Usage

### Sensor

The sensor `sensor.ha_no_service` will be available with:
- **State**: The rejection reason text
- **Attributes**:
  - `reason`: The full rejection text

### Service

Call the service to manually get a new rejection reason:

```yaml
service: ha_no_service.get_no
```

### Example Automations

**Daily morning rejection:**
```yaml
automation:
  - alias: "Daily No"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      - service: ha_no_service.get_no
      - service: notify.mobile_app
        data:
          title: "Today's Rejection Reason"
          message: "{{ states('sensor.ha_no_service') }}"
```

**Use in your dashboard:**
```yaml
type: entities
entities:
  - entity: sensor.ha_no_service
    name: "Need an excuse?"
```

## API Information

This integration uses the [No-as-a-Service API](https://naas.isalman.dev/no):
- **Endpoint**: `https://naas.isalman.dev/no`
- **Rate Limit**: 120 requests per minute per IP
- **Response**: `{"reason": "rejection reason text"}`

## Credits

- **API Provider**: [no-as-a-service](https://github.com/hotheadhacker/no-as-a-service) by [@hotheadhacker](https://github.com/hotheadhacker)
- **API Endpoint**: [naas.isalman.dev](https://naas.isalman.dev/no)

## License

MIT License - see [LICENSE](LICENSE) for details.

This integration is not affiliated with or endorsed by the no-as-a-service project.

---

[commits-shield]: https://img.shields.io/github/commit-activity/y/Diondk/ha_no_service.svg?style=for-the-badge
[commits]: https://github.com/Diondk/ha_no_service/commits/master
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/Diondk/ha_no_service.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/Diondk/ha_no_service.svg?style=for-the-badge
[releases]: https://github.com/Diondk/ha_no_service/releases
