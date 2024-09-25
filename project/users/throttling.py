from rest_framework.throttling import SimpleRateThrottle


class ApiKeyRateThrottle(SimpleRateThrottle):
    scope = "apikey"

    def get_cache_key(self, request, view):
        apikey = request.headers.get("apikey")
        return self.cache_format % {
            'scope': self.scope,
            'ident': apikey
        }

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()
