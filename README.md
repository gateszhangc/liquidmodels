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
- `INFRA_REPO_TOKEN`: GitHub token with write access to `gateszhangc/liquidmodels-infra`.

The workflow uses the per-run `GITHUB_TOKEN` for application checkout inside the Kubernetes build Job and GHCR push authentication. Production requires a stable `ghcr-pull` dockerconfigjson secret in the `liquidmodels` namespace with GHCR read access.

## Search Console

`liquidmodels.lol` is managed as a Google Search Console Domain Property. Verify ownership with a Cloudflare DNS TXT record, then submit:

```text
https://liquidmodels.lol/sitemap.xml
```

Do not add GA4, Clarity, or other analytics scripts unless the analytics policy changes.
