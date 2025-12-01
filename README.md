# [Maybe Material for Zed](https://zed.dev/extensions/maybe-material)

> [!NOTE]
> **New:** Use Maybe Material with [Prism](https://prismjs.com/): [prism/](prism/)

> **🩷 Curated vibrant and harmonious themes in various colors, schemes and contrast options.** It's like Not Material's older sister.
> 
> Red, yellow, green, blue, purple, cyan. Light and dark, two contrast options, three background options. 72 variations in total.
>
> [Install latest version - v0.1.0](https://zed.dev/extensions/maybe-material)

Version 2 of my [Not Material theme](https://zed.dev/extensions/not-material-theme) that makes heavy use of the HCT colour
space to create pleasing, harmonious and accessible themes.

![Sunset Standard theme](sunset-standard.png)
_**Sunset.** Pretty, Material-inspired themes._

![Amethyst Standard theme](amethyst-standard.png)
_**Amethyst.** One of six different colours._

![Honey Standard theme](honey-standard.png)
_**Honey.** With light and dark, high contrast and low contrast, opaque, transparent or blurred, there's a theme for everyone._

## Get started

Either:

- [Install Maybe Material from the Zed extension store.](https://zed.dev/extensions/maybe-material)
- [Install the extension/ folder as a dev extension.](https://zed.dev/docs/extensions/developing-extensions#developing-an-extension-locally)
- Move [themes/maybe-material.json](./extension/themes/maybe-material.json) into your [Zed themes folder](https://zed.dev/docs/themes#local-themes).

## Themes

> [!IMPORTANT]
> Transparent and blurred variants are still being worked on. They might not
> look quite right.

As previously stated, there are:

- Two schemes: light and dark
- Two contrast options: standard and high
- Three background options: opaque, transparent and blurred

And, there are six colours:

- 🌇 Red - Sunrise and Sunset
- 🍯 Yellow - Honey and Amber
- 🌿 Green - Mint and Jade
- 👔 Blue - Workspace and Blueprint
- 🪻 Purple - Lavender and Amethyst
- 🩵 Cyan - Valerate and Cypionate

## For tinkerers

> [!IMPORTANT]
> `zed-hct-theme-maker` hasn't been published yet.

Maybe Material is built on `zed-hct-theme-maker` and some hastily thrown
together Python scripts. So, you'll need Python 3.

- [modules/theme.m.kdl](./modules/theme.m.kdl) and [modules/roles.m.kdl](./modules/roles.m.kdl) contain colour tokens and their mappings to Zed elements
- [fixed-tokens.json](./fixed-tokens.json) contains a set of fixed colours that don't change (i.e "red")
- [variations.json](./variations.json) contains the theme colours and their names.
- [gen-palettes.py](./gen-palettes.py) is the code to generate palettes from [fixed-tokens.json](./fixed-tokens.json) and [variations.json](./variations.json).
- [gen-root.py](./gen-root.py) generates [maybe-material.kdl](./maybe-material.kdl).

There's a Makefile, so after you're done tinkering, all you need to do is:

```sh
make build
```
