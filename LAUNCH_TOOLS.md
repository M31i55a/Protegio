# Lancer les Outils depuis le Dashboard

## 🎯 Vue d'ensemble

Vous pouvez maintenant lancer tous vos outils de sécurité directement depuis le dashboard de PROTEGIO. Les applications sont accessibles de deux façons:

### 1. Cartes d'Application dans le Dashboard
Les 8 outils principaux sont affichés sous forme de cartes cliquables à la page d'accueil du dashboard. Cliquez sur n'importe quelle carte pour accéder à l'outil.

### 2. Menu Latéral (Sidebar)
Tous les outils sont également listés dans le menu latéral gauche sous la section "Tools & Applications" pour un accès rapide.

---

## 📋 Liste des Outils Disponibles

### 1. **Checker** - Vérification d'Informations
- **URL:** `/checker/`
- **Icône:** Loupe
- **Description:** Vérifier les informations et valider les configurations
- **Fonction:** Effectue des vérifications détaillées sur les systèmes

### 2. **DNS Tool** - Outils DNS Avancés
- **URL:** `/dns_tool/`
- **Icône:** Globe
- **Description:** Outils DNS et résolution de domaines
- **Fonction:** NSLookup, Dig et autres requêtes DNS

### 3. **Scanner** - Scanner de Vulnérabilités
- **URL:** `/scanner/`
- **Icône:** Radar
- **Description:** Scanner de sécurité et détection de vulnérabilités
- **Fonction:** Scans de sécurité automatisés avec rapports ZAP

### 4. **Intruder** - Tests de Pénétration
- **URL:** `/intruder/`
- **Icône:** Cadenas
- **Description:** Tests de pénétration et attaques automatisées
- **Fonction:** Simule des attaques pour tester la résilience

### 5. **Protegio Tools** - Outils de Protection
- **URL:** `/protegioTools/`
- **Icône:** Bouclier
- **Description:** Outils de protection et renforcement
- **Fonction:** WHOIS, géolocalisation IP, et analyses de domaine

### 6. **Performance** - Analyse de Performance
- **URL:** `/perforNet/`
- **Icône:** Tachymètre
- **Description:** Tests de performance réseau
- **Fonction:** Speedtest, latence, bande passante

### 7. **Reports** - Rapports de Sécurité
- **URL:** `/reports/`
- **Icône:** Fichier PDF
- **Description:** Accédez à tous vos rapports générés
- **Fonction:** Visualisez, téléchargez vos rapports ZAP

### 8. **Intégrations** - Intégrations Externes
- **URL:** `/integrations/`
- **Icône:** Puzzle
- **Description:** Intégrations avec d'autres outils
- **Fonction:** Nuclei, Port Scanner, SSL/TLS Checker

---

## 🚀 Actions Rapides

Le dashboard inclut également des **Actions Rapides** en bas pour accéder rapidement aux fonctions les plus utilisées:

1. **Nouveau Scan** → Lance un nouveau scan de vulnérabilités
2. **Télécharger Rapport** → Accès à vos rapports de sécurité
3. **Paramètres** → Configuration et préférences
4. **Vérifications** → Vérifications rapides du système

---

## 🎮 Comment Utiliser

### Depuis le Dashboard Principal

1. **Login** à `http://localhost:8000/accounts/login/`
   - Username: `admin`
   - Password: `admin123456`

2. **Accédez au Dashboard** à `http://localhost:8000/dashboard/`

3. **Cliquez sur une Application**
   - Utilisez les cartes colorées pour accéder aux outils
   - Les cartes ont un effet de survol interactif
   - Les actions rapides au bas vous donnent accès rapide

4. **Utilisez le Menu Latéral**
   - Section "Tools & Applications" pour accès direct
   - Tous les outils sont listés avec des icônes distinctes

---

## 📊 Navigation Intégrée

Chaque outil est maintenant complètement intégré au dashboard:

- ✅ Authentification requise (protection par login)
- ✅ Thème sombre uniforme avec PROTEGIO
- ✅ Navigation fluide entre les applications
- ✅ Accès rapide via sidebar
- ✅ Menu principal pour retour au dashboard

---

## 🔐 Sécurité

- Tous les outils requirent une **authentification**
- Seuls les utilisateurs connectés peuvent accéder
- Les admins ont un accès supplémentaire aux outils spécialisés
- Sessions sécurisées avec CSRF protection

---

## 💾 Rapports

La nouvelle application **Reports** vous permet de:

1. **Lister tous vos rapports** - Page complète avec liste
2. **Visualiser en détail** - Voir les rapports directs dans le navigateur
3. **Télécharger** - Exporter vos rapports en HTML
4. **Filtrer et rechercher** - Organisez vos rapports

### URL de Rapports
- Lister: `/reports/`
- Voir: `/reports/view/<filename>/`
- Télécharger: `/reports/download/<filename>/`

---

## 🔗 Architecture

```
Dashboard (/)
├── Checker (/checker/)
├── DNS Tool (/dns_tool/)
├── Scanner (/scanner/)
├── Intruder (/intruder/)
├── Protegio Tools (/protegioTools/)
├── Performance (/perforNet/)
├── Reports (/reports/)
└── Intégrations (/integrations/)
```

---

## ✨ Fonctionnalités Ajoutées

### Dashboard
- ✅ Cartes d'application cliquables
- ✅ Navigation vers tous les outils
- ✅ Actions rapides
- ✅ Statistiques en temps réel

### Sidebar
- ✅ Liens vers tous les outils
- ✅ Section "Tools & Applications"
- ✅ Icônes distinctives
- ✅ Accès rapide

### Application Reports
- ✅ Liste de tous les rapports
- ✅ Visualisation en ligne
- ✅ Téléchargement de rapports
- ✅ Métadonnées (date, taille)

---

## 🎨 Expérience Utilisateur

- **Cartes Interactives:** Survol pour voir l'effet de zoom
- **Navigation Fluide:** Liens directs vers chaque outil
- **Thème Unifié:** Design sombre professionnel
- **Responsive:** Fonctionne sur tous les appareils

---

## 📝 Notes Techniques

### URLs Rajoutées:
```python
# Dans unified_tool/urls.py
path('reports/', include('apps.reports.urls')),
```

### Vues Mises à Jour:
- Dashboard avec URLs correctes pour chaque outil
- Reports app avec views pour lister, voir et télécharger

### Templates Générées:
- `reports/list.html` - Liste de rapports
- `reports/view.html` - Visualisation de rapport
- Dashboard mis à jour avec liens cliquables

---

## 🚀 Prochaines Étapes

1. **Test des Outils** - Testez les liens depuis le dashboard
2. **Génération de Rapports** - Lancez un scan pour générer des rapports
3. **Visualisation** - Consultez vos rapports dans la section Reports
4. **Personnalisation** - Modifiez les URLs ou ajoutez de nouveaux outils

---

## ✅ Checklist de Configuration

- ✅ Dashboard mis à jour avec URLs
- ✅ Sidebar mise à jour avec liens
- ✅ Application Reports créée
- ✅ URLs principales configurées
- ✅ Settings mis à jour
- ✅ Templates créées et stylisées
- ✅ Authentification intégrée

---

**Statut:** ✅ **OPÉRATIONNEL**

Vous pouvez maintenant lancer tous vos outils depuis le dashboard!

Pour installer un nouvel outil:
1. Créez son app Django
2. Ajoutez l'URL à `unified_tool/urls.py`
3. Mettez à jour le dashboard `apps_menu` avec l'URL
4. Mettez à jour le sidebar dans `base.html`
