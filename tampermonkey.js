```javascript
// ==UserScript==
// @name         A.I Script
// @namespace    https://github.com/palopdt-sketch
// @version      1.0.7
// @description  A.I Script - YouTube Player Block + Auto Update
// @match        https://www.youtube.com/*
// @match        https://www.youtube-nocookie.com/*
// @match        https://www.google.com/*
// @match        https://www.google.com.vn/*
// @match        https://google.com/*
// @match        https://google.vn/*
// @updateURL    https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/tampermonkey.js
// @downloadURL  https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/tampermonkey.js
// @connect      raw.githubusercontent.com
// @connect      youtube.com
// @connect      google.com
// @grant        GM_xmlhttpRequest
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';

    // =========================================================
    // CẤU HÌNH
    // =========================================================

    // 1 = BẬT chặn YouTube Player
    // 0 = TẮT chặn YouTube Player

    const BLOCK_PLAYER = 1;

    // Phiên bản hiện tại
    const CURRENT_VERSION = '1.0.7';

    // GitHub Update URL
    const UPDATE_URL =
        'https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/tampermonkey.js';

    // Kiểm tra update mỗi 10 phút
    const UPDATE_INTERVAL = 10 * 60 * 1000;

    const LOG_PREFIX = '[A.I Script]';

    // =========================================================
    // LOG
    // =========================================================

    function log(...args) {
        console.log(LOG_PREFIX, ...args);
    }

    function error(...args) {
        console.error(LOG_PREFIX, ...args);
    }

    log('Version:', CURRENT_VERSION);
    log('Block Player:', BLOCK_PLAYER ? 'ON' : 'OFF');
    log('URL:', location.href);

    // =========================================================
    // VERSION COMPARE
    // =========================================================

    function compareVersion(v1, v2) {

        const a = String(v1)
            .replace(/^v/i, '')
            .split('.')
            .map(Number);

        const b = String(v2)
            .replace(/^v/i, '')
            .split('.')
            .map(Number);

        for (
            let i = 0;
            i < Math.max(a.length, b.length);
            i++
        ) {

            const n1 = a[i] || 0;
            const n2 = b[i] || 0;

            if (n1 > n2) return 1;
            if (n1 < n2) return -1;
        }

        return 0;
    }

    // =========================================================
    // AUTO UPDATE
    // =========================================================

    let updateChecking = false;

    function checkUpdate() {

        if (updateChecking) {
            return;
        }

        updateChecking = true;

        log('Checking GitHub update...');

        GM_xmlhttpRequest({

            method: 'GET',

            url: UPDATE_URL + '?_=' + Date.now(),

            headers: {
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            },

            timeout: 15000,

            onload: function (response) {

                updateChecking = false;

                if (response.status !== 200) {

                    error(
                        'Update failed. HTTP:',
                        response.status
                    );

                    return;
                }

                const source = response.responseText;

                const match = source.match(
                    /@version\s+([^\s]+)/i
                );

                if (!match) {

                    error(
                        'Cannot find @version.'
                    );

                    return;
                }

                const remoteVersion =
                    match[1].trim();

                log(
                    'Local:',
                    CURRENT_VERSION,
                    '| Remote:',
                    remoteVersion
                );

                if (
                    compareVersion(
                        remoteVersion,
                        CURRENT_VERSION
                    ) > 0
                ) {

                    log(
                        'NEW VERSION:',
                        remoteVersion
                    );

                    localStorage.setItem(
                        'AI_SCRIPT_PENDING_UPDATE',
                        source
                    );

                    localStorage.setItem(
                        'AI_SCRIPT_PENDING_VERSION',
                        remoteVersion
                    );

                    alert(
                        'A.I Script có phiên bản mới!\n\n' +
                        'Hiện tại: ' +
                        CURRENT_VERSION +
                        '\n' +
                        'Mới: ' +
                        remoteVersion
                    );

                    setTimeout(() => {
                        location.reload();
                    }, 1000);

                } else {

                    log(
                        'No update available.'
                    );
                }
            },

            ontimeout: function () {

                updateChecking = false;

                error(
                    'Update timeout.'
                );
            },

            onerror: function (err) {

                updateChecking = false;

                error(
                    'Update error:',
                    err
                );
            }
        });
    }

    // =========================================================
    // YOUTUBE PLAYER SELECTORS
    // =========================================================

    const YOUTUBE_PLAYER_SELECTORS = [

        '#movie_player',

        '#player',

        '#ytd-player',

        'ytd-player',

        '.html5-video-player',

        'video.html5-main-video',

        '#player-container-outer',

        '#player-container-inner',

        'ytd-watch-flexy #player'
    ];

    // =========================================================
    // INJECT CSS
    // =========================================================

    function injectYouTubeCSS() {

        // BLOCK_PLAYER = 0
        // Không làm gì

        if (BLOCK_PLAYER !== 1) {
            return;
        }

        if (
            !location.hostname.includes(
                'youtube.com'
            )
        ) {
            return;
        }

        if (
            document.getElementById(
                'ai-script-youtube-block'
            )
        ) {
            return;
        }

        const style =
            document.createElement('style');

        style.id =
            'ai-script-youtube-block';

        style.textContent = `

            #movie_player,
            #player,
            #ytd-player,
            ytd-player,
            .html5-video-player,
            video.html5-main-video,
            #player-container-outer,
            #player-container-inner,
            ytd-watch-flexy #player {

                display: none !important;

                visibility: hidden !important;

                opacity: 0 !important;

                pointer-events: none !important;
            }

        `;

        (
            document.head ||
            document.documentElement
        ).appendChild(style);
    }

    // =========================================================
    // HIDE YOUTUBE PLAYER
    // =========================================================

    function hideYouTubePlayer() {

        // =====================================================
        // QUAN TRỌNG:
        // BLOCK_PLAYER = 0
        // => THOÁT NGAY
        // =====================================================

        if (BLOCK_PLAYER !== 1) {
            return;
        }

        if (
            !location.hostname.includes(
                'youtube.com'
            )
        ) {
            return;
        }

        YOUTUBE_PLAYER_SELECTORS
            .forEach(selector => {

                document
                    .querySelectorAll(selector)
                    .forEach(el => {

                        el.style.setProperty(
                            'display',
                            'none',
                            'important'
                        );

                        el.style.setProperty(
                            'visibility',
                            'hidden',
                            'important'
                        );

                        el.style.setProperty(
                            'opacity',
                            '0',
                            'important'
                        );

                        el.style.setProperty(
                            'pointer-events',
                            'none',
                            'important'
                        );
                    });
            });

        // Chặn video HTML5

        document
            .querySelectorAll('video')
            .forEach(video => {

                try {
                    video.pause();
                } catch (e) {}

                video.style.setProperty(
                    'display',
                    'none',
                    'important'
                );

                video.style.setProperty(
                    'visibility',
                    'hidden',
                    'important'
                );

                video.style.setProperty(
                    'opacity',
                    '0',
                    'important'
                );

                video.style.setProperty(
                    'pointer-events',
                    'none',
                    'important'
                );
            });
    }

    // =========================================================
    // GOOGLE
    // =========================================================

    function handleGoogle() {

        if (
            !location.hostname.includes(
                'google.'
            )
        ) {
            return;
        }

        log('Google detected.');
    }

    // =========================================================
    // MAIN
    // =========================================================

    function run() {

        // Chỉ inject CSS khi BLOCK_PLAYER = 1
        injectYouTubeCSS();

        // Chỉ block player khi BLOCK_PLAYER = 1
        hideYouTubePlayer();

        handleGoogle();
    }

    run();

    // =========================================================
    // YOUTUBE SPA
    // =========================================================

    let lastURL = location.href;

    setInterval(() => {

        if (location.href !== lastURL) {

            lastURL = location.href;

            log(
                'URL changed:',
                location.href
            );

            setTimeout(run, 100);
            setTimeout(run, 500);
            setTimeout(run, 1500);
        }

        // BLOCK_PLAYER = 1 mới xử lý
        if (BLOCK_PLAYER === 1) {
            hideYouTubePlayer();
        }

    }, 500);

    // =========================================================
    // MUTATION OBSERVER
    // =========================================================

    const observer =
        new MutationObserver(() => {

            if (BLOCK_PLAYER === 1) {
                hideYouTubePlayer();
            }

        });

    function startObserver() {

        if (!document.documentElement) {

            setTimeout(
                startObserver,
                100
            );

            return;
        }

        observer.observe(
            document.documentElement,
            {
                childList: true,
                subtree: true
            }
        );
    }

    startObserver();

    // =========================================================
    // AUTO UPDATE
    // =========================================================

    // Kiểm tra ngay khi mở trang
    checkUpdate();

    // Sau đó kiểm tra mỗi 10 phút
    setInterval(
        checkUpdate,
        UPDATE_INTERVAL
    );

})();
```
