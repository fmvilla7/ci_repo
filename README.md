# fleet-api

Mini-service de supervision d'une flotte de robots d'entrepôt.

Ce dépôt est le **fil rouge** du module *Usine Logicielle et CI/CD* (ESIA A3). Vous
allez le faire grossir séance après séance jusqu'à disposer d'une chaîne
d'intégration et de déploiement complète.

---

## Ce que fait le service

Les robots d'un entrepôt émettent régulièrement leur télémétrie : tension
batterie, position, état de charge. `fleet-api` la reçoit et en calcule des
indicateurs — niveau de charge, autonomie restante, distance parcourue, alertes
batterie, agrégats de flotte.

Le cœur métier vit dans `src/fleet_api/telemetry.py` : une dizaine de
**fonctions pures**, sans état ni entrée-sortie, donc directement testables.

## Démarrage

Prérequis : [uv](https://docs.astral.sh/uv/). Inutile d'installer Python vous-même :
uv télécharge la version voulue (≥ 3.12) au premier `uv sync`.

```bash
uv sync                 # installe les dépendances
uv run pytest -v        # lance la suite de tests
```

Vous devez obtenir **6 tests au vert**. Si ce n'est pas le cas, signalez-le
avant d'aller plus loin.

## Structure

```
src/fleet_api/
├── models.py       Position, Reading, RobotState
├── telemetry.py    les fonctions de calcul  ← l'objet du TD 1
├── store.py        stockage en mémoire ou PostgreSQL  (séance 5)
└── api.py          les endpoints HTTP                 (séance 5)
tests/
└── test_telemetry.py   3 tests d'exemple, le reste est à écrire
```

## Règles du jeu

1. **Les docstrings font foi.** Elles sont la spécification. Quand le code et la
   docstring divergent, c'est le code qui a tort. Ne modifiez jamais une
   docstring pour la faire coller à l'implémentation.
2. **On travaille par pull request.** À partir de la séance 2, `main` est
   protégée : plus de push direct.
3. **Un commit, une intention.** Le message dit *pourquoi*, pas *quoi* — le diff
   dit déjà quoi.

## Backlog

Évolutions possibles pour le rendu final, par ordre de difficulté croissante.
Vous n'avez pas à toutes les traiter : mieux vaut deux fonctionnalités bien
testées et bien intégrées que six bâclées.

- [ ] `GET /robots/{id}/history` — historique de télémétrie d'un robot
- [ ] Alerte sur immobilité prolongée (aucun déplacement depuis N minutes)
- [ ] `GET /fleet/heatmap` — densité de présence par zone de l'entrepôt
- [ ] Estimation du temps de charge restant
- [ ] Détection de dérive de calibration entre robots d'un même modèle
- [ ] Export Prometheus des indicateurs de flotte

## Progression du module

| Séance | Ce que vous ajoutez |
|---|---|
| 1 | Les tests manquants, un premier workflow |
| 2 | Pipeline lint / test / build, protection de `main` |
| 3 | Workflow réutilisable, pre-commit, Dependabot |
| 4 | Dockerfile multi-stage, docker compose |
| 5 | Build et publication d'image sur GHCR, scan de vulnérabilités |
| 6 | Couverture, typage, analyse statique, quality gate |
| 7 | Release versionnée, environnements, bascule et retour arrière |
| 8 | Revue croisée, finalisation |


Cache Froid : 50s
Cache Chaud : 16s
48. Cache restored successfully

src/fleet_api/telemetry.py	battery_percentage	 	      100%	4	0	0	100%	2	0	100%
src/fleet_api/telemetry.py	is_low_battery	 	            0%	1	1	0	 	100%	0	0	0%
src/fleet_api/telemetry.py	distance_m	 	               100%	1	0	0	100%	0	0	100%
src/fleet_api/telemetry.py	path_length_m	 	            0%	4	4	0	 	0%	2	0	 	0%
src/fleet_api/telemetry.py	average_speed_mps	 	         0%	3	3	0	 	0%	2	0	 	0%
src/fleet_api/telemetry.py	estimate_runtime_minutes	 	0%	3	3	0	 	0%	2	0	 	0%
src/fleet_api/telemetry.py	median_voltage_mv	 	         0%	3	3	0	 	0%	2	0	 	0%
src/fleet_api/telemetry.py	robot_state	 	               0%	7	7	0	 	0%	6	0	 	0%
src/fleet_api/telemetry.py	detect_voltage_dropouts	 	   0%	6	6	0	 	0%	4	0	 	0%
src/fleet_api/telemetry.py	fleet_summary	 	            0%	2	2	0	 	100%	0	0	0%
src/fleet_api/telemetry.py	(no function)	 	            100%	18	0	0	100%	0	0	100%
