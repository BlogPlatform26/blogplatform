from django.conf import settings


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not getattr(settings, "CSP_ENABLED", True):
            return response

        header_name = "Content-Security-Policy"
        if getattr(settings, "CSP_REPORT_ONLY", False):
            header_name = "Content-Security-Policy-Report-Only"

        if header_name not in response:
            policy = self.build_policy(getattr(settings, "CSP_DIRECTIVES", {}))
            if policy:
                response[header_name] = policy

        return response

    def build_policy(self, directives):
        parts = []

        for directive, values in directives.items():
            if values is None:
                continue

            if isinstance(values, str):
                values = [values]

            clean_values = []
            for value in values:
                value = str(value).strip()
                if value:
                    clean_values.append(value)

            if clean_values:
                parts.append(f"{directive} {' '.join(clean_values)}")
            else:
                parts.append(directive)

        return "; ".join(parts)
