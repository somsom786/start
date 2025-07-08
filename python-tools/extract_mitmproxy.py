from mitmproxy import http

def request(flow: http.HTTPFlow):
    if "x.com/i/api/graphql" in flow.request.pretty_url:
        with open("x_api_dump.txt", "a") as f:
            f.write(f"{flow.request.method} {flow.request.pretty_url}\n")
            f.write("Headers:\n")
            for k, v in flow.request.headers.items():
                f.write(f"{k}: {v}\n")
            f.write("Body:\n")
            f.write(flow.request.get_text() + "\n")
            f.write("-" * 80 + "\n")
#this code is used to extract mitmproxy as a readable file
