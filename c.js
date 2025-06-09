const tweetnacl = require('./tweetnacl.js')();
const blake2b = require('./blake2b.js')();

let $e = 237;
let public_key = "91b03050a79fb0148debef99bcd76494707018c3005a90d1a4eab63e1f38bc20";
let password = "PASSWORD";
let timestamp = Math.floor(Date.now() / 1000).toString();

let j = 64;
var k = 1;
var l = 1;
var m = 1;
var n = 2;
var o = 32;
var p = 16;

function decodeUTF8(a) {
    if (typeof a !== "string") {
        throw new TypeError(`expected string, got ${typeof a}`);
    }
    var b;
    a = unescape(encodeURIComponent(a));
    var c = new Uint8Array(a.length);
    for (b = 0; b < a.length; b++) {
        c[b] = a.charCodeAt(b);
    }

    return c;
}

function formatPublicKey(a) {
    var b = [];
    for (var c = 0; c < a.length; c += 2) {
        b.push(parseInt(a.slice(c, c + 2), 16));
    }
    return new Uint8Array(b);
}

function blake2ba(a, b) {
    var c = blake2b.blake2bInit(tweetnacl.box.nonceLength, null);
    blake2b.blake2bUpdate(c, a);
    blake2b.blake2bUpdate(c, b);
    return blake2b.blake2bFinal(c);
}

function ha(a) {
    for (var b = 0; b < a.length; b++) {
        a[b] = 0
    }
}

function seal(a, b) {
    var c = new Uint8Array(48 + a.length);
    var e = tweetnacl.box.keyPair();
    c.set(e.publicKey);
    var i = Object(blake2ba)(e.publicKey, b);
    a = tweetnacl.box(a, i, b, e.secretKey);
    c.set(a, e.publicKey.length);
    Object(ha)(e.secretKey);
    return c;
}

// a = 237
// d = public_key
// e = password_uint8Array
// f = timestamp_uint8Array
function encrypt(a, d, e, f) {
    var g = 100 + e.length;
    if (d.length != j) {
        throw new Error("public key is not a valid hex string");
    }

    var t = formatPublicKey(d);
    if (!t) {
        throw new Error("public key is not a valid hex string");
    }

    var u = new Uint8Array(g);
    var v = 0;
    u[v] = k;
    v += l;
    u[v] = a;
    v += m;
    d = {
        name: "AES-GCM",
        length: o * 8,
    };
    var w = {
        name: "AES-GCM",
        iv: new Uint8Array(12),
        additionalData: f,
        tagLen: p,
    };

    return crypto.subtle
    .generateKey(d, true, ["encrypt", "decrypt"])
    .then(function (a) {
        var c = crypto.subtle.exportKey("raw", a);
        a = crypto.subtle.encrypt(w, a, e.buffer);
        return Promise.all([c, a]);
    })
    .then(function (a) {
        var b = new Uint8Array(a[0]);
        b = seal(b, t);
        u[v] = b.length & 255;
        u[v + 1] = (b.length >> 8) & 255;
        v += n;
        u.set(b, v);
        v += o;
        v += 48;
        if (b.length !== o + 48) {
            throw new Error("encrypted key is the wrong length");
        }
        b = new Uint8Array(a[1]);
        a = b.slice(-p);
        b = b.slice(0, -p);
        u.set(a, v);
        v += p;
        u.set(b, v);

        return u;
    });
}

function encodeBase64(a) {
    var b, c = [], d = a.length;
    for (b = 0; b < d; b++) {
        c.push(String.fromCharCode(a[b]));
    }
    return btoa(c.join(""));
}

function encryptPassword (a, b, e, f, g, j) {
    e = decodeUTF8(e.toString());
    var k = decodeUTF8(f.toString());
    return encrypt(a, b, e, k)
    .then(function (a) {
        return [j, g, f, encodeBase64(a)].join(":");
    });
}

(async () => {
    const $e = process.argv[2];
    const public_key = process.argv[3];
    const password = process.argv[4];
    const timestamp = process.argv[5];
    const result = await encryptPassword($e, public_key, password, timestamp, 10, "#PWD_INSTAGRAM_BROWSER");
    console.log(result);
})();