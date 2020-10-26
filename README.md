# Pocket 센서

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.4][version-shield]

Pocket Sensor for Home Assistant 입니다.<br>
file을 읽어들여 파일의 목록을 sensor로 생성하여 줍니다.<br>
pocket은 일정한 주기로 목록에 있는 값을 상태값으로 반영하여 줍니다.<br>

switch 1개와 pocket에 지정한 갯수만큼의 pocket sensor가 생성됩니다.<br>
switch의 경우, on인 동안에는 업데이트 시에 파일을 읽어들여 목록을 반영합니다.<br>
off로 되어 있는 경우, 이미 존재하는 목록 내에서 상태를 반영합니다.<br>

![screenshot_1](https://github.com/miumida/pocket/blob/master/images/pocket.png?raw=true)<br>

파일은 '주소' 목록과 '제목|주소' 목록으로 생성할 수 있다.<br>

![screenshot_1](https://github.com/miumida/pocket/blob/master/images/Screenshot1.png?raw=true)<br>
![screenshot_1](https://github.com/miumida/pocket/blob/master/images/Screenshot2.png?raw=true)<br>

<br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2020.06.02  | First version  |
| v1.0.1  | 2020.10.26  | Add Attributes now_key, now_val  |


<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components 에 파일을 넣어줍니다.<br>
  `<config directory>/custom_components/pocket/__init__.py`<br>
  `<config directory>/custom_components/pocket/manifest.json`<br>
  `<config directory>/custom_components/pocket/switch.py`<br>
- configuration.yaml 파일에 설정을 추가합니다.<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > Integrations 메뉴 선택
- 우측 상단 메뉴 버튼 클릭 후 Custom repositories 선택
- Add Custom Repository URL 에 'https://github.com/miumida/pocket' 입력,<br>
  Category에 Integration 선택 후 ADD
- HACS > Integrations 메뉴에서 우측 하단 + 버튼 누르고 [KR] Pocket 검색하여 설치

<br>

## Usage
### configuration
- HA 설정에 whitelist_external_dirs 속성을 추가해주고 경로를 추가한다.
```yaml
# Example configuration.yaml entry
homeassistant:
  whitelist_external_dirs:
     - /config
     - /config/playlist

#media_extractor 추가필요(용도에 따라)
media_extractor:
```
- HA 설정에 pocket sensor를 추가합니다.<br>
```yaml
# Example configuration.yaml entry
switch:
  - platform: pocket
    scan_interval: 200
    pockets:
      - id: 'yul2song'
        name: '율이재생목록'
        file_path: /config/pocket.txt
      - id: 'miumida4song'
        name: '재생목록1'
        file_path: /config/miumida4song.txt
      - id: 'doctorlist'
        name: '슬의생ost'
        file_path: /config/playlist/doctorlife.txt    
```


### Automation example
media_player의 상태가 playing에서 idle로 변경되면 서비스 호출하여 재생
```yaml
automation:
- id: 'autoplay'
  alias: 자동재생
  description: ''
  trigger:
  - entity_id: media_player.mini
    from: playing
    platform: state
    to: idle
  condition: []
  action:
  - data_template:
      media_content_id: '{{ states.sensor.pocket_miumida4song.state }}'
      media_content_type: video
    entity_id: media_player.mini
    service: media_extractor.play_media
```


### Script example
재생목록1 재생
```yaml
script:
  'playlist1_play':
    alias: 재생목록1 재생
    sequence:
    - data_template:
        media_content_id: '{{ states.sensor.pocket_miumida4song.state }}'
        media_content_type: video
      entity_id: media_player.mini
      service: media_extractor.play_media
    - data: {}
      entity_id: automation.jadongjaesaeng
      service: automation.turn_on
```


<br><br>
### 기본 설정값

|옵션|내용|
|--|--|
|platform| (필수) pocket|
|scan_interval| (옵션) Sensor Update Term / default(900s) |
|pockets| (옵션) 포켓 리스트 |
<br>

### pockets 설정값
|옵션|내용|
|--|--|
|id| (필수) pocket 목록 id|
|name| (필수) pocket 목록 이름 |
|file_path| (필수) 파일경로 |

[version-shield]: https://img.shields.io/badge/version-v1.0.1-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
