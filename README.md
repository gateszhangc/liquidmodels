# Liquid Models

Independent static guide for Liquid models, Liquid Foundation Models, and efficient edge-to-cloud AI deployment.

## Local Development

```bash
npm ci
npm test
npm start
```

The site runs on `http://127.0.0.1:3000` by default and exposes `/healthz` for Kubernetes probes.

## Production Route

- Application repository: `gateszhangc/liquidmodels`
- Branch: `main`
- Image: `ghcr.io/gateszhangc/liquidmodels:<git-sha>`
- GitOps repository: `gateszhangc/liquidmodels-infra`
- Production overlay: `apps/liquidmodels/overlays/production`
- Dokploy project: none

Deployment flow:

```text
GitHub Actions -> K8s build Job -> GHCR -> kustomization newTag -> ArgoCD automatic sync
```

Required GitHub Actions secrets:

- `KUBECONFIG_B64`: base64-encoded kubeconfig that can create build jobs and update secrets in the build namespace.
- `SOURCE_REPO_TOKEN`: GitHub token with read access to `gateszhangc/liquidmodels`.
- `GHCR_USERNAME`: GitHub username used for GHCR push auth.
- `GHCR_TOKEN`: GitHub token with `write:packages` permission.
- `INFRA_REPO_TOKEN`: GitHub token with write access to `gateszhangc/liquidmodels-infra`.

## Search Console

`liquidmodels.lol` is managed as a Google Search Console Domain Property. Verify ownership with a Cloudflare DNS TXT record, then submit:

```text
https://liquidmodels.lol/sitemap.xml
```

Do not add GA4, Clarity, or other analytics scripts unless the analytics policy changes.
