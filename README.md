![](docs/catpuccin_moka.png)

# tui-network

`tui-network` is a Python based TUI for managing the wifi on Linux built with [Textual](https://github.com/Textualize/textual).

## Rationale

I've recently started using [i3wm](https://i3wm.org/) on a DE-less Debian install as my main driver and I'm trying to keep it as minimal as possible, getting the most out of the terminal. While I like the simplicity and effectiveness of [nmcli](https://networkmanager.dev/docs/api/latest/nmcli.html), I find it really ugly. After some digging, I finally found the awesome [Impala](https://github.com/pythops/impala), which inspired me to make my own in Python with Textual.

## Themes

You can change the theme by hitting `ctrl+p`. A sneak peek at some of them:

![](docs/dark.png)

![](docs/light.png)

![](docs/catpuccin_moka.png)

![](docs/catpuccin_latte.png)

![](docs/nord.png)

## Usage

### Connect to a network
- `enter` on a network to compile the Network Name input field
- insert the passphrase
- `enter` to connect

### Scan for available networks
- `ctrl+s` to start the scan
- `ctrl+r` to refresh the page

### Toggle the wifi power
- `ctrl+u` to power up the wifi
- `ctrl+d` to power down the wifi
- `ctrl+r` to refresh the page

## Dependencies

You need to have `iwd` as your network backend. Visit the [official Debian documentation](https://wiki.debian.org/NetworkManager/iwd) for more details.

## Install

```
git clone https://github.com/Zatfer17/tui-network
cd tui-network
pipx install .
```

## Feature matrix

- [x] Display current wifi network name
- [ ] Show current wifi network signal
- [x] Display available networks
- [ ] Show available networks signal
- [x] Connect to available networks
- [x] Pretty interface
- [x] Refresh shortcut