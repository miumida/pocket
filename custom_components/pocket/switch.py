"""Support for sensor value(s) stored in local files."""
import logging
import os
import random

import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.const import CONF_NAME, CONF_UNIT_OF_MEASUREMENT, CONF_VALUE_TEMPLATE
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Pocket"

CONF_POCKETS     = 'pockets'
CONF_POCKET_ID   = 'id'
CONF_POCKET_NAME = 'name'
CONF_FILE_PATH   = "file_path"

ICON = "mdi:clipboard-text-play-outline"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
        vol.Required(CONF_POCKETS): vol.All(cv.ensure_list, [{
            vol.Required(CONF_POCKET_ID): cv.string,
            vol.Required(CONF_POCKET_NAME): cv.string,
            vol.Required(CONF_FILE_PATH): cv.isfile,
        }]),
})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the file sensor."""
    pockets    = config.get(CONF_POCKETS)

    switch = pocketSwitch(pockets)

    async_add_entities([switch], True)

    for poc in pockets:
        id   = poc[CONF_POCKET_ID]
        name = poc[CONF_POCKET_NAME]
        path = poc[CONF_FILE_PATH]

        api  = pocketAPI(path)

        if hass.config.is_allowed_path(path):
            async_add_entities([FileSensor(id, name, path, api, switch)], True)
        else:
            _LOGGER.error("'%s' is not awhitelisted directory", path)


class pocketSwitch(SwitchEntity):
    """Representation of a Pocket Switch."""

    def __init__(self, pockets):
        """Initialize the Pocket Switch."""
        self._is_on   = False
        self._pockets = pockets

    @property
    def entity_id(self):
        """Return the entity ID."""
        return 'switch.pocket_auto_loading'

    @property
    def name(self):
        """Name of the device."""
        return 'Pocket File Auto Loading'

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:map-marker-question'

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False

    @property
    def device_info(self):
        return {
            'identifiers': {
                # Serial numbers are unique identifiers within a specific domain
                ('POCKET', 'POCKET')
            },
            'name': 'pocket',
            'manufacturer': 'miumida',
            'model': 'pocket',
            'sw_version': '0.0.1',
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attrs = {}

        for poc in self._pockets:
            id   = poc[CONF_POCKET_ID]
            name = poc[CONF_POCKET_NAME]

            attrs[id] = name

        return attrs

    def update(self):
        """Get the latest value"""
        self._is_on = self._is_on


class FileSensor(Entity):
    """Implementation of a file sensor."""

    def __init__(self, id, name, path, api, switch):
        """Initialize the file sensor."""
        self._id        = id
        self._name      = name
        self._file_path = path
        self._state     = None
        self._data      = {}

        self._switch    = switch
        self._api       = api

    @property
    def entity_id(self):
        """Return the entity ID."""
        return 'sensor.pocket_{}'.format(self._id)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Get the latest entry from a file and updates the state."""

        if len(self._data) > 0:
            if not self._switch._is_on:
                tmp = list(self._data.values())

                random.shuffle(tmp)

                data = random.sample(tmp,1)[0]

                if (self._state == data):
                    random.shuffle(tmp)
                    random.shuffle(tmp)
                    data = random.sample(tmp, 1)[0]

                self._state = data

                return

        self._api.load_file()

        self._data = self._api._data

        tmp = list(self._data.values())

        random.shuffle(tmp)
        data = random.sample(tmp,1)[0]

        if (self._state == data):
            random.shuffle(tmp)
            random.shuffle(tmp)
            data = random.sample(tmp,1)[0]

        self._state = data

    @property
    def device_state_attributes(self):
        """Attributes."""
        return self._data

class pocketAPI:
    """pocketAPI."""

    def __init__(self, path):
        """Initialize the pocketAPI."""
        self._path = path
        self._data = {}

    def load_file(self):
        try:
            temp = []
            pk   = {}
            cnt  = 0

            if not os.path.exists(self._path):
                _LOGGER.warning("File not exists: %s", seelf._path)

                f = open(self._path, 'w')
                f.write("n/a")
                f.close()

            with open(self._path, encoding="utf-8") as file_data:
                for line in file_data:
                    data = line

                    if "|" in data:
                        arr = data.split("|")
                        pk[arr[0]] = arr[1].strip()
                    else:
                        pk[str(cnt)] = data.strip()
                        cnt += 1

                self._data = pk

        except (IndexError, FileNotFoundError, IsADirectoryError, UnboundLocalError):
            _LOGGER.warning(
                "File or data not present at the moment: %s",
                os.path.basename(self._path),
            )
            return

