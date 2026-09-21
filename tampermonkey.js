// ==UserScript==
// @name         A.I Script
// @namespace    https://github.com/palopdt-sketch
// @version      1.0.5
// @description  A.I Script - Block YouTube Player
// @match        https://www.youtube.com/*
// @match        https://www.youtube-nocookie.com/*
// @match        https://www.google.com/*
// @match        https://www.google.com.vn/*
// @match        https://google.com/*
// @match        https://www.google.vn/*
// @updateURL    https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/tampermonkey.js
// @downloadURL  https://raw.githubusercontent.com/palopdt-sketch/hosts/refs/heads/main/tampermonkey.js
// @connect      youtube.com
// @connect      google.com
// @grant        GM_xmlhttpRequest
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';

    console.log('[A.I Script] 1.0.5 loaded:', location.href);

    // =========================================================
    // CHẶN / ẨN YOUTUBE PLAYER
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

    function hideYouTubePlayer() {
        if (!location.hostname.includes('youtube.com')) {
            return;
        }

        YOUTUBE_PLAYER_SELECTORS.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => {
                el.style.setProperty('display', 'none', 'important');
                el.style.setProperty('visibility', 'hidden', 'important');
                el.style.setProperty('opacity', '0', 'important');
                el.style.setProperty('pointer-events', 'none', 'important');
            });
        });

        // Chặn video HTML5 nếu YouTube tạo lại player
        document.querySelectorAll('video').forEach(video => {
            video.pause();

            video.style.setProperty('display', 'none', 'important');
            video.style.setProperty('visibility', 'hidden', 'important');
            video.style.setProperty('opacity', '0', 'important');

            try {
                video.removeAttribute('src');
                video.load();
            } catch (e) {
                console.debug('[A.I Script] Cannot clear video:', e);
            }
        });
    }

    // =========================================================
    // CSS CHẶN PLAYER
    // =========================================================

    function injectYouTubeCSS() {
        if (!location.hostname.includes('youtube.com')) {
            return;
        }

        if (document.getElementById('ai-script-youtube-block')) {
            return;
        }

        const style = document.createElement('style');
        style.id = 'ai-script-youtube-block';

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

        (document.head || document.documentElement).appendChild(style);
    }

    // =========================================================
    // GOOGLE
    // =========================================================

    function handleGoogle() {
        if (!location.hostname.includes('google.')) {
            return;
        }

        console.log('[A.I Script] Google detected');
    }

    // =========================================================
    // CHẠY
    // =========================================================

    function run() {
        injectYouTubeCSS();
        hideYouTubePlayer();
        handleGoogle();
    }

    run();

    // =========================================================
    // YOUTUBE SPA
    // YouTube chuyển trang mà không reload website
    // =========================================================

    let lastUrl = location.href;

    setInterval(() => {
        if (location.href !== lastUrl) {
            lastUrl = location.href;

            console.log('[A.I Script] URL changed:', location.href);

            setTimeout(run, 100);
            setTimeout(run, 500);
            setTimeout(run, 1500);
        }

        hideYouTubePlayer();
    }, 500);

    // =========================================================
    // THEO DÕI DOM
    // Nếu YouTube tự tạo lại player thì tiếp tục ẩn
    // =========================================================

    const observer = new MutationObserver(() => {
        hideYouTubePlayer();
    });

    function startObserver() {
        if (!document.documentElement) {
            setTimeout(startObserver, 100);
            return;
        }

        observer.observe(document.documentElement, {
            childList: true,
            subtree: true
        });
    }

    startObserver();

})();
