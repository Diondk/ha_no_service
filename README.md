# HA No Service

A Home Assistant integration for [hotheadhacker/no-as-a-service](https://github.com/hotheadhacker/no-as-a-service) - Get creative rejection reasons for saying "no".

## Features

- **Sensor**: Displays random rejection reasons from over 1,000+ pre-written excuses
- **Service**: Manual refresh service to get a new rejection reason
- **Attributes**:
  - `reason`: The rejection reason text

## Installation

1. Copy the `ha_no_service` folder to your `custom_components` directory
2. Add to your `configuration.yaml`:

```yaml
sensor:
  - platform: ha_no_service
```

3. Restart Home Assistant

## Usage

### Sensor

The sensor `sensor.ha_no_service` will automatically update every hour with a new rejection reason.

### Service

Call the `ha_no_service.get_no` service to manually fetch a new rejection reason:

```yaml
service: ha_no_service.get_no
```

### Example Automation

```yaml
automation:
  - alias: "Get Daily No"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      - service: ha_no_service.get_no
      - service: notify.mobile_app
        data:
          title: "Today's Rejection"
          message: "{{ states('sensor.ha_no_service') }}"
```

## API

This integration uses the [No-as-a-Service API](https://naas.isalman.dev/no) which returns random rejection reasons from a collection of 1,000+ pre-written excuses.

**API Details:**
- Endpoint: `https://naas.isalman.dev/no`
- Rate Limit: 120 requests per minute per IP
- Response Format: `{"reason": "rejection reason text"}`

## Credits

- Project: [hotheadhacker/no-as-a-service](https://github.com/hotheadhacker/no-as-a-service)
- API: [naas.isalman.dev](https://naas.isalman.dev/no)
