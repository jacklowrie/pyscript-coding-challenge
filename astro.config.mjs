// @ts-check
import { defineConfig } from "astro/config";

import icon from "astro-icon";

// https://astro.build/config
export default defineConfig({
  site: "https://jacklowrie.github.io",
  base: "/pyscript-coding-challenge",
  integrations: [icon()],
});
