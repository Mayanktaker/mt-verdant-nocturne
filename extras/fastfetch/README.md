# MT Verdant Nocturne — Fastfetch Showcase

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Custom Fastfetch configuration with custom nocturnal botanical ASCII logo and theme palette.

## Usage
Run directly:
```sh
fastfetch -c extras/fastfetch/config.jsonc
```

Or install as your default Fastfetch setup:
```sh
mkdir -p ~/.config/fastfetch
cp extras/fastfetch/config.jsonc ~/.config/fastfetch/config.jsonc
cp extras/fastfetch/mt-verdant.txt ~/.config/fastfetch/mt-verdant.txt
sed -i 's|"extras/fastfetch/mt-verdant.txt"|"~/.config/fastfetch/mt-verdant.txt"|' ~/.config/fastfetch/config.jsonc
```
