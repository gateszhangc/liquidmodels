# Liquid Models Launch Checklist

## DNS and TLS

- Add `liquidmodels.lol` to Cloudflare.
- Replace Porkbun nameservers with the two Cloudflare nameservers.
- Point the apex record to the Kubernetes ingress or load balancer.
- Redirect `www.liquidmodels.lol` to `https://liquidmodels.lol/`.
- Use Cloudflare SSL mode `Full (strict)` and enable Always Use HTTPS.

## Google Search Console

- Create a Domain Property for `liquidmodels.lol`.
- Add the Google TXT verification record in Cloudflare DNS.
- Wait for GSC ownership verification to pass.
- Submit `https://liquidmodels.lol/sitemap.xml`.
- Request indexing for `https://liquidmodels.lol/`.

## Production Verification

Run these after ArgoCD has synced the production overlay:

```bash
dig +short NS liquidmodels.lol
curl -I http://liquidmodels.lol
curl -I https://liquidmodels.lol
curl -L https://liquidmodels.lol/robots.txt
curl -L https://liquidmodels.lol/sitemap.xml
```

Expected results:

- Nameservers are Cloudflare nameservers.
- HTTP redirects to HTTPS.
- HTTPS returns `200`.
- The homepage is the Liquid Models static site, not the Porkbun parked page.
- `robots.txt` references `https://liquidmodels.lol/sitemap.xml`.
- No GA4, Clarity, or Google Tag Manager script is present.
