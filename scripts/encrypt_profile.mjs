#!/usr/bin/env node
/**
 * Encrypts private_src/profile_body.html & private_src/lenses_snippet.js
 * into data/profile.enc.json using W3C WebCrypto PBKDF2-SHA256 + AES-256-GCM.
 * Ensures ZERO plaintext resume/career strings exist in git-tracked files.
 */

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath, pathToFileURL } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SITE_ROOT = path.resolve(__dirname, "..");
const PRIV_DIR = path.join(SITE_ROOT, "private_src");
const OUT_FILE = path.join(SITE_ROOT, "data", "profile.enc.json");

const ITERATIONS = 210000;

async function main() {
  const htmlPath = path.join(PRIV_DIR, "profile_body.html");
  const lensesPath = path.join(PRIV_DIR, "lenses_snippet.js");
  if (!fs.existsSync(htmlPath) || !fs.existsSync(lensesPath)) {
    throw new Error("Missing private_src/profile_body.html or lenses_snippet.js");
  }

  const keyFile = path.join(PRIV_DIR, "access_key.txt");
  let accessKey = process.env.PROFILE_KEY || "";
  if (!accessKey && fs.existsSync(keyFile)) {
    accessKey = fs.readFileSync(keyFile, "utf8").trim();
  }
  if (!accessKey) {
    // 144-bit URL-safe random access code (never matches cloud secret prefixes)
    accessKey = "ak-cv-" + crypto.randomBytes(18).toString("base64url");
    fs.writeFileSync(keyFile, accessKey + "\n", "utf8");
  }

  const htmlBody = fs.readFileSync(htmlPath, "utf8");
  const { LENSES } = await import(pathToFileURL(lensesPath).href);

  const plaintextBytes = new TextEncoder().encode(
    JSON.stringify({ html: htmlBody, lenses: LENSES })
  );

  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);

  const baseKey = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(accessKey),
    "PBKDF2",
    false,
    ["deriveKey"]
  );

  const aesKey = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: ITERATIONS, hash: "SHA-256" },
    baseKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt"]
  );

  const ctBuf = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    aesKey,
    plaintextBytes
  );

  const payload = {
    v: 1,
    alg: "AES-256-GCM",
    kdf: "PBKDF2-SHA256",
    iter: ITERATIONS,
    salt: Buffer.from(salt).toString("base64"),
    iv: Buffer.from(iv).toString("base64"),
    ct: Buffer.from(ctBuf).toString("base64")
  };

  fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
  fs.writeFileSync(OUT_FILE, JSON.stringify(payload, null, 2) + "\n", "utf8");

  const shareMd = `# Private Executive Profile — Secret Shareable Links

Keep this file private (excluded via \`.gitignore\`). Anyone with these exact URLs will unlock your Executive Profile automatically in the browser (\`AES-256-GCM\`), while anyone visiting \`/profile/\` without \`#k=...\` cannot access or inspect the content.

- **Access Key:** \`${accessKey}\`
- **Unified Executive Profile:** https://kenseiamit.github.io/profile/#k=${accessKey}
- **AI Solutions Architect View:** https://kenseiamit.github.io/profile/?lens=architect#k=${accessKey}
- **Staff AI & Systems Engineer View:** https://kenseiamit.github.io/profile/?lens=staff#k=${accessKey}
- **Senior AI/ML & MLOps View:** https://kenseiamit.github.io/profile/?lens=mlops#k=${accessKey}
- **AI Engineering Leadership View:** https://kenseiamit.github.io/profile/?lens=leadership#k=${accessKey}

To rotate/revoke this link at any time, delete \`private_src/access_key.txt\`, run \`node scripts/encrypt_profile.mjs\`, commit \`data/profile.enc.json\`, and push.
`;
  fs.writeFileSync(path.join(PRIV_DIR, "SECRET_SHARE_LINKS.md"), shareMd, "utf8");
  console.log(`Encrypted profile -> ${OUT_FILE} (${(fs.statSync(OUT_FILE).size / 1024).toFixed(1)} KB)`);
  console.log(`Secret URL: https://kenseiamit.github.io/profile/#k=${accessKey}`);
}

main();
