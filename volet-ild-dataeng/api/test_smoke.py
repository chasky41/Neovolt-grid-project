"""
Smoke test de l'API Néovolt Grid+ (volet ILD).
Vérifie que chaque endpoint répond et renvoie une structure cohérente, sans
lancer de serveur (TestClient en mémoire).

Lancer depuis volet-ild-dataeng/api/ :
    ..\\..\\.venv\\Scripts\\python.exe test_smoke.py
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def check(name, resp, predicate):
    ok = resp.status_code == 200 and predicate(resp.json())
    print(f"  [{'OK ' if ok else 'FAIL'}] {name} -> {resp.status_code}")
    return ok

def main():
    results = []
    r = client.get("/health")
    results.append(check("/health", r, lambda j: j["status"] == "ok" and j["releves"] > 0))
    print("        periode:", r.json().get("periode"))

    r = client.get("/zones")
    results.append(check("/zones", r, lambda j: len(j) == 8))

    r = client.get("/qualite")
    results.append(check("/qualite", r, lambda j: j["releves_total"] > 0))
    print("        qualité:", r.json())

    r = client.get("/pdl/PDL-000001")
    results.append(check("/pdl/PDL-000001", r, lambda j: j["id_pdl"] == "PDL-000001"))

    r = client.get("/pdl/PDL-000001/consommation", params={"debut": "2024-01-01", "fin": "2024-01-31"})
    results.append(check("/pdl/.../consommation", r, lambda j: j["n"] > 0))

    r = client.get("/consommation/par-zone", params={"zone": "Centre-Ville", "debut": "2024-01-01", "fin": "2024-01-07"})
    results.append(check("/consommation/par-zone", r, lambda j: j["n"] > 0))

    r = client.get("/fraude")
    results.append(check("/fraude", r, lambda j: j["nb_cas"] == 24))

    r = client.get("/incidents")
    results.append(check("/incidents", r, lambda j: len(j["par_type"]) > 0))

    r = client.get("/pdl/PDL-INEXISTANT")
    ok404 = r.status_code == 404
    print(f"  [{'OK ' if ok404 else 'FAIL'}] /pdl/INEXISTANT (404 attendu) -> {r.status_code}")
    results.append(ok404)

    n_ok = sum(1 for x in results if x)
    print(f"\n=== {n_ok}/{len(results)} tests OK ===")
    raise SystemExit(0 if n_ok == len(results) else 1)

if __name__ == "__main__":
    main()
