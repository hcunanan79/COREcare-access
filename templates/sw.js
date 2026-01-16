const CACHE_NAME = 'corecare-v1';
const OFFLINE_URL = '/portal/offline/';

const ASSETS_TO_CACHE = [
    OFFLINE_URL,
    '/static/manifest.json',
    '/static/images/icon-192.png',
    '/static/images/icon-512.png',
    // Add CSS/JS bundles here if they have stable URLs
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

self.addEventListener('fetch', (event) => {
    // Only handle GET requests for now
    if (event.request.method !== 'GET') return;

    event.respondWith(
        fetch(event.request)
            .catch(() => {
                return caches.match(event.request).then((response) => {
                    if (response) {
                        return response;
                    }
                    // If request is for a page navigation, return offline page
                    if (event.request.mode === 'navigate') {
                        return caches.match(OFFLINE_URL);
                    }
                    return null;
                });
            })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME) {
                    return caches.delete(key);
                }
            }));
        })
    );
});
