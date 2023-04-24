// ==UserScript==
// @name     LinkedIn Feed Blocker 912381
// @version  1
// @grant    none
// @match       *://*.linkedin.com/*
// @run-at      document-start
// ==/UserScript==

window.addEventListener("load", () => {
    document.querySelector('[aria-label="Main Feed"]').style.display = 'none';
});