# Publishing

## Cloudflare Pages

1. Connect the GitHub repository `he20000405-pixel/chonggrok-guides-portal`.
2. Select `main` as the production branch.
3. Use `bundle exec jekyll build` as the build command.
4. Use `_site` as the output directory.
5. Set `RUBY_VERSION` to a Cloudflare-supported Ruby 3.x release.
6. Verify the generated `pages.dev` site before adding a custom domain.
7. Add `guides.chonggrok.com` through Pages > Custom domains. Do not create the DNS record manually first.

## Safety boundary

Only the `guides` subdomain may be created for this project. Do not modify apex, `www`, MX, NS, TXT, DNSSEC, SSL/TLS mode, Workers routes, redirects, cache rules, WAF rules, login, payment or verification settings.

