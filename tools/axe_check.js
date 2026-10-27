#!/usr/bin/env node
/* Automated accessibility scan (axe-core) of every page. Fails on any violation.
 *
 *   npm install --no-save jsdom@30.1.3 axe-core@4.14.0     (CI does this; versions tested)
 *   node tools/axe_check.js
 *
 * Scope and limits: runs in a simulated DOM, so the colour-contrast rule cannot be
 * evaluated and is excluded; automated checks find only part of what a manual review,
 * keyboard test and screen-reader test would. A pass is NOT a claim of WCAG conformance.
 */
const fs = require('fs'), path = require('path');
const { JSDOM } = require('jsdom');
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const root = path.resolve(__dirname, '..');
(async () => {
  const pages = fs.readdirSync(root).filter(f => f.endsWith('.html') && !/^google/.test(f)).sort();
  let failures = 0;
  for (const f of pages) {
    const dom = new JSDOM(fs.readFileSync(path.join(root, f), 'utf8'), { runScripts: 'outside-only', url: 'https://example.test/' + f });
    dom.window.eval(axeSource);
    const r = await dom.window.axe.run(dom.window.document, { rules: { 'color-contrast': { enabled: false } }, resultTypes: ['violations'] });
    for (const v of r.violations) {
      failures++;
      console.log(`${f}: [${v.impact}] ${v.id}: ${v.help}\n    ${v.nodes[0].html.slice(0, 120).replace(/\n/g, ' ')}`);
    }
  }
  console.log(failures ? `\n${failures} accessibility violation(s) in ${pages.length} pages` : `OK: no axe violations in ${pages.length} pages (colour contrast not assessed)`);
  process.exit(failures ? 1 : 0);
})();
