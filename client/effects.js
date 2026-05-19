// Letter-by-letter intro scramble, click-to-burn, hover jitter, periodic wave.
// Runs after Yew has rendered into <main>. No build step — plain JS.

(function () {
  "use strict";

  const SCRAMBLE_CHARS =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%&*<>?/+=";
  const EMBER_CHARS = "*+x.~^!?";

  // Block-level selectors we treat as an independent "textbox" for the intro.
  const BLOCK_SELECTOR =
    "h1, h2, h3, p, li, .brand, .eyebrow, .button, .section h2, .section__note, .section__sub";

  function randChar(pool) {
    const p = pool || SCRAMBLE_CHARS;
    return p[Math.floor(Math.random() * p.length)];
  }

  function rectCenter(el) {
    const r = el.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2, rect: r };
  }

  // Wrap every visible character inside `root` in a <span class="ch"> while
  // keeping whole words inside <span class="word"> so wrapping behaves
  // naturally and inline-block letters don't break mid-word.
  function wrapTextNodes(root) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(n) {
        if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        const p = n.parentNode;
        if (!p) return NodeFilter.FILTER_REJECT;
        if (p.nodeType !== 1) return NodeFilter.FILTER_REJECT;
        if (p.classList && (p.classList.contains("ch") || p.classList.contains("word"))) {
          return NodeFilter.FILTER_REJECT;
        }
        const tag = p.nodeName;
        if (tag === "SCRIPT" || tag === "STYLE" || tag === "CANVAS" || tag === "NOSCRIPT") {
          return NodeFilter.FILTER_REJECT;
        }
        if (p.closest && p.closest(".boids-background")) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });

    const targets = [];
    let node;
    while ((node = walker.nextNode())) targets.push(node);

    for (const n of targets) {
      const frag = document.createDocumentFragment();
      const pieces = n.nodeValue.split(/(\s+)/);
      for (const piece of pieces) {
        if (!piece) continue;
        if (/^\s+$/.test(piece)) {
          frag.appendChild(document.createTextNode(piece));
          continue;
        }
        const word = document.createElement("span");
        word.className = "word";
        for (const ch of piece) {
          const c = document.createElement("span");
          c.className = "ch";
          c.dataset.final = ch;
          c.textContent = ch;
          word.appendChild(c);
        }
        frag.appendChild(word);
      }
      n.parentNode.replaceChild(frag, n);
    }
  }

  // Animate a single .ch through random characters then settle on its final
  // letter. `delay` is in ms from now, `duration` is the scramble length.
  function scrambleSpan(span, delay, duration) {
    if (!span || !span.isConnected) return;
    const final = span.dataset.final;
    if (final === undefined) return;
    if (span._scramble) cancelAnimationFrame(span._scramble);

    span.classList.add("ch--scrambling");
    span.textContent = randChar();
    const start = performance.now() + delay;
    let lastSwap = 0;

    const step = (now) => {
      if (!span.isConnected) return;
      if (now < start) {
        span._scramble = requestAnimationFrame(step);
        return;
      }
      const t = (now - start) / duration;
      if (t >= 1) {
        span.textContent = final;
        span.classList.remove("ch--scrambling");
        span._scramble = null;
        return;
      }
      if (now - lastSwap > 26 + Math.random() * 40) {
        span.textContent = randChar();
        lastSwap = now;
      }
      span._scramble = requestAnimationFrame(step);
    };
    span._scramble = requestAnimationFrame(step);
  }

  // Run the intro: each block-level text element scrambles as its own unit,
  // ordered top-left → bottom-right, with letters cascading within.
  function runIntro() {
    const allChars = Array.from(document.querySelectorAll(".ch"));
    if (!allChars.length) return;

    const blocks = new Set();
    for (const ch of allChars) {
      const owner = ch.closest(BLOCK_SELECTOR) || ch.parentElement;
      if (owner) blocks.add(owner);
    }

    const blockList = Array.from(blocks);
    blockList.sort((a, b) => {
      const ra = a.getBoundingClientRect();
      const rb = b.getBoundingClientRect();
      if (Math.abs(ra.top - rb.top) > 6) return ra.top - rb.top;
      return ra.left - rb.left;
    });

    const BLOCK_GAP = 70;     // ms between blocks starting
    const CHAR_GAP = 14;      // ms between letters within a block
    const BASE_DUR = 520;
    const JITTER_DUR = 380;

    blockList.forEach((block, bi) => {
      const chars = Array.from(block.querySelectorAll(".ch")).filter(
        (c) => c.closest(BLOCK_SELECTOR) === block
      );
      const blockDelay = bi * BLOCK_GAP;
      chars.forEach((c, ci) => {
        scrambleSpan(c, blockDelay + ci * CHAR_GAP, BASE_DUR + Math.random() * JITTER_DUR);
      });
    });
  }

  // Burn every .ch within `radius` pixels of (x, y), then re-scramble back in.
  function burnAt(x, y, radius) {
    const spans = document.querySelectorAll(".ch");
    const toRestore = [];
    spans.forEach((s) => {
      if (s.classList.contains("ch--burning")) return;
      const r = s.getBoundingClientRect();
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      const dist = Math.hypot(cx - x, cy - y);
      if (dist <= radius) {
        const angle = Math.atan2(cy - y, cx - x);
        s.style.setProperty("--burn-dx", `${Math.cos(angle) * 18}px`);
        s.style.setProperty("--burn-dy", `${-12 - Math.random() * 18}px`);
        s.style.setProperty("--burn-rot", `${(Math.random() - 0.5) * 60}deg`);
        s.classList.add("ch--burning");
        toRestore.push(s);
      }
    });
    const burnMs = 700;
    setTimeout(() => {
      for (const s of toRestore) {
        s.classList.remove("ch--burning");
        s.style.removeProperty("--burn-dx");
        s.style.removeProperty("--burn-dy");
        s.style.removeProperty("--burn-rot");
        scrambleSpan(s, Math.random() * 90, 320 + Math.random() * 260);
      }
    }, burnMs);
  }

  function spawnEmbers(x, y, count) {
    const wrap = document.createElement("div");
    wrap.className = "ember-wrap";
    wrap.style.left = `${x}px`;
    wrap.style.top = `${y}px`;
    const n = count || 14;
    for (let i = 0; i < n; i++) {
      const e = document.createElement("span");
      e.className = "ember";
      const angle = (Math.PI * 2 * i) / n + Math.random() * 0.6;
      const dist = 50 + Math.random() * 110;
      const life = 700 + Math.random() * 600;
      e.style.setProperty("--dx", `${Math.cos(angle) * dist}px`);
      e.style.setProperty("--dy", `${Math.sin(angle) * dist - 30}px`);
      e.style.setProperty("--life", `${life}ms`);
      e.style.animationDelay = `${Math.random() * 80}ms`;
      e.textContent = randChar(EMBER_CHARS);
      wrap.appendChild(e);
    }
    document.body.appendChild(wrap);
    setTimeout(() => wrap.remove(), 1700);
  }

  function attachClicks() {
    let lastBurn = 0;
    document.addEventListener("click", (e) => {
      const t = e.target;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA")) return;
      burnAt(e.clientX, e.clientY, 120);
      spawnEmbers(e.clientX, e.clientY, 14);
    });

    // Hold + drag = flamethrower trail. Throttled so it doesn't melt the CPU.
    let dragging = false;
    document.addEventListener("mousedown", () => {
      dragging = true;
    });
    document.addEventListener("mouseup", () => {
      dragging = false;
    });
    document.addEventListener("mousemove", (e) => {
      if (!dragging) return;
      const now = performance.now();
      if (now - lastBurn < 70) return;
      lastBurn = now;
      burnAt(e.clientX, e.clientY, 80);
      spawnEmbers(e.clientX, e.clientY, 6);
    });
  }

  function attachHoverJitter() {
    document.addEventListener("mouseover", (e) => {
      const t = e.target;
      if (t && t.classList && t.classList.contains("ch")) {
        if (t.classList.contains("ch--burning")) return;
        t.classList.add("ch--jitter");
      }
    });
    document.addEventListener("mouseout", (e) => {
      const t = e.target;
      if (t && t.classList && t.classList.contains("ch")) {
        setTimeout(() => t.classList.remove("ch--jitter"), 280);
      }
    });
  }

  // Soft horizontal ripple that walks across letters near a random Y band
  // every few seconds. Cheap and ambient.
  function startWave() {
    setInterval(() => {
      const spans = document.querySelectorAll(".ch");
      if (!spans.length) return;
      const yOrigin = Math.random() * window.innerHeight;
      const BAND = 60;
      spans.forEach((s) => {
        if (s.classList.contains("ch--burning")) return;
        const r = s.getBoundingClientRect();
        const dy = Math.abs(r.top + r.height / 2 - yOrigin);
        if (dy > BAND) return;
        const delay = r.left * 0.45 + Math.random() * 30;
        setTimeout(() => {
          s.classList.add("ch--wave");
          setTimeout(() => s.classList.remove("ch--wave"), 420);
        }, delay);
      });
    }, 9000);
  }

  function start() {
    wrapTextNodes(document.querySelector(".site-header"));
    wrapTextNodes(document.querySelector("main"));
    wrapTextNodes(document.querySelector(".site-footer"));
    runIntro();
    attachClicks();
    attachHoverJitter();
    startWave();
  }

  function waitForYew() {
    const ready = () => {
      const main = document.querySelector("main");
      return main && main.childElementCount > 0;
    };
    if (ready()) {
      start();
      return;
    }
    const obs = new MutationObserver(() => {
      if (ready()) {
        obs.disconnect();
        setTimeout(start, 60);
      }
    });
    obs.observe(document.body, { childList: true, subtree: true });
    setTimeout(() => {
      if (!document.querySelector(".ch") && ready()) {
        obs.disconnect();
        start();
      }
    }, 4000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", waitForYew);
  } else {
    waitForYew();
  }
})();
