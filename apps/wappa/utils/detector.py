import requests
from bs4 import BeautifulSoup
import re

SIGNATURES = {

    # ═══════════════════════════════
    # CMS
    # ═══════════════════════════════
    "WordPress": {
        "category": "CMS",
        "icon": "https://cdn.simpleicons.org/wordpress/21759B",
        "html": [r"wp-content", r"wp-includes"],
        "version": [r"ver=(\d+\.\d+[\.\d]*)"],
    },
    "Drupal": {
        "category": "CMS",
        "icon": "https://cdn.simpleicons.org/drupal/0678BE",
        "html": [r"Drupal\.settings", r"/sites/default/files/"],
        "headers": {"x-generator": r"Drupal"},
        "version": [r"Drupal ([\d\.]+)"],
    },
    "Joomla": {
        "category": "CMS",
        "icon": "https://cdn.simpleicons.org/joomla/5091CD",
        "html": [r"/media/jui/", r"joomla"],
        "version": [r"Joomla! ([\d\.]+)"],
    },
    "Ghost": {
        "category": "CMS",
        "icon": "https://cdn.simpleicons.org/ghost/15171A",
        "html": [r"ghost\.io", r"content=\"Ghost"],
        "version": [r"Ghost/([\d\.]+)"],
    },
    "Wix": {
        "category": "CMS",
        "icon": "https://cdn.simpleicons.org/wix/000000",
        "html": [r"wixsite\.com", r"X-Wix-Published-Version"],
    },
    "Squarespace": {
        "category": "CMS",
        "icon": "https://cdn.simpleicons.org/squarespace/000000",
        "html": [r"squarespace\.com", r"static\.squarespace\.com"],
    },
    "Webflow": {
        "category": "CMS",
        "icon": "https://cdn.simpleicons.org/webflow/4353FF",
        "html": [r"webflow\.com", r"Webflow"],
    },

    # ═══════════════════════════════
    # E-COMMERCE
    # ═══════════════════════════════
    "Shopify": {
        "category": "E-commerce",
        "icon": "https://cdn.simpleicons.org/shopify/96BF48",
        "html": [r"Shopify\.shop", r"cdn\.shopify\.com"],
        "headers": {"x-shopid": r".+"},
    },
    "WooCommerce": {
        "category": "E-commerce",
        "icon": "https://cdn.simpleicons.org/woocommerce/96588A",
        "html": [r"woocommerce", r"wc-cart"],
    },
    "Magento": {
        "category": "E-commerce",
        "icon": "https://cdn.simpleicons.org/magento/EE672F",
        "html": [r"Mage\.Cookies", r"skin/frontend/"],
    },
    "PrestaShop": {
        "category": "E-commerce",
        "icon": "https://cdn.simpleicons.org/prestashop/DF0067",
        "html": [r"prestashop", r"/modules/ps_"],
        "version": [r"prestashop/([\d\.]+)"],
    },
    "OpenCart": {
        "category": "E-commerce",
        "icon": "https://cdn.simpleicons.org/opencart/009AC7",
        "html": [r"route=common/home", r"opencart"],
    },

    # ═══════════════════════════════
    # FRAMEWORKS JAVASCRIPT
    # ═══════════════════════════════
    "React": {
        "category": "Framework JavaScript",
        "icon": "https://cdn.simpleicons.org/react/61DAFB",
        "html": [r"data-reactroot", r"__REACT"],
        "scripts": [r"react[\.\-]([\d\.]+)\.min\.js", r"react-dom"],
        "version": [r"react[@/]([\d\.]+)"],
    },
    "Vue.js": {
        "category": "Framework JavaScript",
        "icon": "https://cdn.simpleicons.org/vuedotjs/4FC08D",
        "html": [r"v-bind", r"v-model", r"__vue__"],
        "scripts": [r"vue[\.\-]([\d\.]+)\.min\.js"],
        "version": [r"vue[@/]([\d\.]+)"],
    },
    "Angular": {
        "category": "Framework JavaScript",
        "icon": "https://cdn.simpleicons.org/angular/DD0031",
        "html": [r"ng-version=\"([\d\.]+)\"", r"\[ng-"],
        "version": [r"ng-version=\"([\d\.]+)\""],
    },
    "Next.js": {
        "category": "Framework JavaScript",
        "icon": "https://cdn.simpleicons.org/nextdotjs/000000",
        "html": [r"__NEXT_DATA__", r"_next/static"],
        "version": [r"\"version\":\"([\d\.]+)\""],
    },
    "Nuxt.js": {
        "category": "Framework JavaScript",
        "icon": "https://cdn.simpleicons.org/nuxtdotjs/00DC82",
        "html": [r"__NUXT__", r"_nuxt/"],
    },
    "Svelte": {
        "category": "Framework JavaScript",
        "icon": "https://cdn.simpleicons.org/svelte/FF3E00",
        "html": [r"__svelte", r"svelte-"],
    },
    "Ember.js": {
        "category": "Framework JavaScript",
        "icon": "https://cdn.simpleicons.org/emberdotjs/E04E39",
        "html": [r"ember\.js", r"Ember\.VERSION"],
        "version": [r"Ember ([\d\.]+)"],
    },
    "Backbone.js": {
        "category": "Framework JavaScript",
        "icon": "https://cdn.simpleicons.org/backbonedotjs/0071B5",
        "html": [r"backbone\.js", r"Backbone\.VERSION"],
    },

    # ═══════════════════════════════
    # BIBLIOTHÈQUES JAVASCRIPT
    # ═══════════════════════════════
    "jQuery": {
        "category": "Bibliothèque JavaScript",
        "icon": "https://cdn.simpleicons.org/jquery/0769AD",
        "html": [r"jquery"],
        "scripts": [r"jquery[\.\-]([\d\.]+)(\.min)?\.js"],
        "version": [r"jquery[\.\-]([\d\.]+)\.min\.js", r"jQuery v([\d\.]+)"],
    },
    "jQuery UI": {
        "category": "Bibliothèque JavaScript",
        "icon": "https://cdn.simpleicons.org/jquery/0769AD",
        "scripts": [r"jquery-ui[\.\-]([\d\.]+)\.min\.js"],
        "version": [r"jquery-ui[\.\-]([\d\.]+)"],
    },
    "Lodash": {
        "category": "Bibliothèque JavaScript",
        "icon": "https://cdn.simpleicons.org/lodash/3492FF",
        "scripts": [r"lodash[\.\-]([\d\.]+)\.min\.js"],
        "version": [r"lodash/([\d\.]+)"],
    },
    "Moment.js": {
        "category": "Bibliothèque JavaScript",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "scripts": [r"moment[\.\-]([\d\.]+)\.min\.js"],
    },
    "D3.js": {
        "category": "Bibliothèque JavaScript",
        "icon": "https://cdn.simpleicons.org/d3dotjs/F9A03C",
        "scripts": [r"d3[\.\-]([\d\.]+)\.min\.js"],
    },
    "Three.js": {
        "category": "Bibliothèque JavaScript",
        "icon": "https://cdn.simpleicons.org/threedotjs/000000",
        "scripts": [r"three[\.\-]([\d\.]+)\.min\.js", r"three\.min\.js"],
    },
    "Alpine.js": {
        "category": "Bibliothèque JavaScript",
        "icon": "https://cdn.simpleicons.org/alpinedotjs/8BC0D0",
        "html": [r"x-data", r"x-bind", r"alpine"],
        "scripts": [r"alpinejs"],
    },
    "HTMX": {
        "category": "Bibliothèque JavaScript",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"hx-get", r"hx-post", r"htmx"],
        "scripts": [r"htmx"],
    },

    # ═══════════════════════════════
    # FRAMEWORKS CSS
    # ═══════════════════════════════
    "Bootstrap": {
        "category": "Framework CSS",
        "icon": "https://cdn.simpleicons.org/bootstrap/7952B3",
        "html": [r"bootstrap\.min\.css", r"bootstrap\.min\.js"],
        "version": [r"bootstrap[\.\-]([\d\.]+)\.min"],
    },
    "Tailwind CSS": {
        "category": "Framework CSS",
        "icon": "https://cdn.simpleicons.org/tailwindcss/06B6D4",
        "html": [r"tailwind"],
        "scripts": [r"tailwind"],
    },
    "Bulma": {
        "category": "Framework CSS",
        "icon": "https://cdn.simpleicons.org/bulma/00D1B2",
        "html": [r"bulma"],
        "scripts": [r"bulma"],
    },
    "Foundation": {
        "category": "Framework CSS",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"foundation\.min\.css", r"zurb-foundation"],
    },
    "Materialize": {
        "category": "Framework CSS",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"materialize\.min\.css", r"materialize"],
    },

    # ═══════════════════════════════
    # SERVEURS WEB
    # ═══════════════════════════════
    "Nginx": {
        "category": "Serveur Web",
        "icon": "https://cdn.simpleicons.org/nginx/009639",
        "headers": {"server": r"nginx[/]?([\d\.]+)?"},
        "version": [r"nginx/([\d\.]+)"],
    },
    "Apache": {
        "category": "Serveur Web",
        "icon": "https://cdn.simpleicons.org/apache/D22128",
        "headers": {"server": r"apache[/]?([\d\.]+)?"},
        "version": [r"Apache/([\d\.]+)"],
    },
    "LiteSpeed": {
        "category": "Serveur Web",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "headers": {"server": r"litespeed"},
    },
    "IIS": {
        "category": "Serveur Web",
        "icon": "https://cdn.simpleicons.org/microsoft/5E5E5E",
        "headers": {"server": r"Microsoft-IIS[/]?([\d\.]+)?"},
        "version": [r"IIS/([\d\.]+)"],
    },
    "Caddy": {
        "category": "Serveur Web",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "headers": {"server": r"caddy"},
    },

    # ═══════════════════════════════
    # LANGAGES & BACKEND
    # ═══════════════════════════════
    "PHP": {
        "category": "Langage",
        "icon": "https://cdn.simpleicons.org/php/777BB4",
        "headers": {"x-powered-by": r"php[/]?([\d\.]+)?"},
        "version": [r"PHP/([\d\.]+)"],
    },
    "Python": {
        "category": "Langage",
        "icon": "https://cdn.simpleicons.org/python/3776AB",
        "headers": {"x-powered-by": r"python"},
    },
    "Ruby": {
        "category": "Langage",
        "icon": "https://cdn.simpleicons.org/ruby/CC342D",
        "headers": {"x-powered-by": r"phusion passenger|ruby"},
    },
    "ASP.NET": {
        "category": "Langage",
        "icon": "https://cdn.simpleicons.org/dotnet/512BD4",
        "headers": {"x-powered-by": r"ASP\.NET", "x-aspnet-version": r".+"},
        "version": [r"ASP\.NET/([\d\.]+)"],
    },

    # ═══════════════════════════════
    # FRAMEWORKS BACKEND
    # ═══════════════════════════════
    "Django": {
        "category": "Framework Backend",
        "icon": "https://cdn.simpleicons.org/django/092E20",
        "headers": {"x-frame-options": r"sameorigin"},
        "html": [r"csrfmiddlewaretoken", r"django"],
    },
    "Laravel": {
        "category": "Framework Backend",
        "icon": "https://cdn.simpleicons.org/laravel/FF2D20",
        "headers": {"x-powered-by": r"laravel"},
        "html": [r"laravel_session", r"laravel"],
    },
    "Ruby on Rails": {
        "category": "Framework Backend",
        "icon": "https://cdn.simpleicons.org/rubyonrails/CC0000",
        "headers": {"x-powered-by": r"phusion passenger"},
        "html": [r"csrf-token.*rails", r"action_dispatch"],
    },
    "Express.js": {
        "category": "Framework Backend",
        "icon": "https://cdn.simpleicons.org/express/000000",
        "headers": {"x-powered-by": r"express"},
    },
    "Spring": {
        "category": "Framework Backend",
        "icon": "https://cdn.simpleicons.org/spring/6DB33F",
        "headers": {"x-application-context": r".+"},
    },

    # ═══════════════════════════════
    # BASES DE DONNÉES
    # ═══════════════════════════════
    "MySQL": {
        "category": "Base de données",
        "icon": "https://cdn.simpleicons.org/mysql/4479A1",
        "html": [r"mysql_error", r"mysqli_"],
    },
    "MongoDB": {
        "category": "Base de données",
        "icon": "https://cdn.simpleicons.org/mongodb/47A248",
        "html": [r"mongodb", r"mongoose"],
    },
    "PostgreSQL": {
        "category": "Base de données",
        "icon": "https://cdn.simpleicons.org/postgresql/4169E1",
        "html": [r"postgresql", r"pg_connect"],
    },
    "Redis": {
        "category": "Base de données",
        "icon": "https://cdn.simpleicons.org/redis/DC382D",
        "html": [r"redis"],
        "headers": {"x-cache": r"redis"},
    },
    "Elasticsearch": {
        "category": "Base de données",
        "icon": "https://cdn.simpleicons.org/elasticsearch/005571",
        "html": [r"elasticsearch"],
    },

    # ═══════════════════════════════
    # CDN & SÉCURITÉ
    # ═══════════════════════════════
    "Cloudflare": {
        "category": "CDN / Sécurité",
        "icon": "https://cdn.simpleicons.org/cloudflare/F38020",
        "headers": {"server": r"cloudflare", "cf-ray": r".+"},
    },
    "Fastly": {
        "category": "CDN / Sécurité",
        "icon": "https://cdn.simpleicons.org/fastly/FF282D",
        "headers": {"x-served-by": r"cache", "via": r"fastly"},
    },
    "Amazon CloudFront": {
        "category": "CDN / Sécurité",
        "icon": "https://cdn.simpleicons.org/amazonaws/FF9900",
        "headers": {"via": r"cloudfront", "x-amz-cf-id": r".+"},
    },
    "Akamai": {
        "category": "CDN / Sécurité",
        "icon": "https://cdn.simpleicons.org/akamai/009BDE",
        "headers": {"x-check-cacheable": r".+", "server": r"akamai"},
    },

    # ═══════════════════════════════
    # OUTILS ANALYTIQUE
    # ═══════════════════════════════
    "Google Analytics": {
        "category": "Analytique",
        "icon": "https://cdn.simpleicons.org/googleanalytics/E37400",
        "html": [r"google-analytics\.com/analytics\.js", r"gtag\(", r"UA-\d+"],
    },
    "Google Tag Manager": {
        "category": "Analytique",
        "icon": "https://cdn.simpleicons.org/googletagmanager/246FDB",
        "html": [r"googletagmanager\.com/gtm\.js"],
    },
    "Matomo": {
        "category": "Analytique",
        "icon": "https://cdn.simpleicons.org/matomo/3152A0",
        "html": [r"matomo\.js", r"piwik\.js"],
    },
    "Hotjar": {
        "category": "Analytique",
        "icon": "https://cdn.simpleicons.org/hotjar/FD3A5C",
        "html": [r"hotjar", r"hjid"],
    },
    "Mixpanel": {
        "category": "Analytique",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"mixpanel\.com/lib", r"mixpanel\.track"],
    },
    "Segment": {
        "category": "Analytique",
        "icon": "https://cdn.simpleicons.org/segment/52BD95",
        "html": [r"cdn\.segment\.com", r"analytics\.load"],
    },
    "Plausible": {
        "category": "Analytique",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"plausible\.io/js"],
    },

    # ═══════════════════════════════
    # OUTILS MARKETING
    # ═══════════════════════════════
    "HubSpot": {
        "category": "Marketing",
        "icon": "https://cdn.simpleicons.org/hubspot/FF7A59",
        "html": [r"hubspot\.com", r"hs-scripts\.com"],
    },
    "Mailchimp": {
        "category": "Marketing",
        "icon": "https://cdn.simpleicons.org/mailchimp/FFE01B",
        "html": [r"mailchimp\.com", r"chimpstatic\.com"],
    },
    "Intercom": {
        "category": "Marketing",
        "icon": "https://cdn.simpleicons.org/intercom/6067F1",
        "html": [r"intercom\.io", r"intercomSettings"],
    },
    "Drift": {
        "category": "Marketing",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"drift\.com/include", r"driftt\.com"],
    },
    "Zendesk": {
        "category": "Marketing",
        "icon": "https://cdn.simpleicons.org/zendesk/03363D",
        "html": [r"zendesk\.com", r"zdassets\.com"],
    },
    "Crisp": {
        "category": "Marketing",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"crisp\.chat", r"client\.crisp\.chat"],
    },
    "Salesforce": {
        "category": "Marketing",
        "icon": "https://cdn.simpleicons.org/salesforce/00A1E0",
        "html": [r"salesforce\.com", r"pardot\.com"],
    },

    # ═══════════════════════════════
    # PUBLICITÉ
    # ═══════════════════════════════
    "Google Ads": {
        "category": "Publicité",
        "icon": "https://cdn.simpleicons.org/googleads/4285F4",
        "html": [r"googleadservices\.com", r"google_conversion"],
    },
    "Facebook Pixel": {
        "category": "Publicité",
        "icon": "https://cdn.simpleicons.org/facebook/1877F2",
        "html": [r"connect\.facebook\.net", r"fbq\("],
    },
    "TikTok Pixel": {
        "category": "Publicité",
        "icon": "https://cdn.simpleicons.org/tiktok/000000",
        "html": [r"analytics\.tiktok\.com", r"ttq\.load"],
    },
    "LinkedIn Insight": {
        "category": "Publicité",
        "icon": "https://cdn.simpleicons.org/linkedin/0A66C2",
        "html": [r"snap\.licdn\.com", r"linkedin\.com/insight"],
    },

    # ═══════════════════════════════
    # HÉBERGEMENT & CLOUD
    # ═══════════════════════════════
    "AWS": {
        "category": "Cloud / Hébergement",
        "icon": "https://cdn.simpleicons.org/amazonaws/FF9900",
        "headers": {"server": r"awselb|amazon", "x-amz-request-id": r".+"},
    },
    "Vercel": {
        "category": "Cloud / Hébergement",
        "icon": "https://cdn.simpleicons.org/vercel/000000",
        "headers": {"x-vercel-id": r".+", "server": r"vercel"},
    },
    "Netlify": {
        "category": "Cloud / Hébergement",
        "icon": "https://cdn.simpleicons.org/netlify/00C7B7",
        "headers": {"x-nf-request-id": r".+", "server": r"netlify"},
    },
    "Heroku": {
        "category": "Cloud / Hébergement",
        "icon": "https://cdn.simpleicons.org/heroku/430098",
        "headers": {"via": r"heroku"},
    },
    "GitHub Pages": {
        "category": "Cloud / Hébergement",
        "icon": "https://cdn.simpleicons.org/github/181717",
        "headers": {"server": r"github\.com"},
    },

    # ═══════════════════════════════
    # SEO & PERFORMANCE
    # ═══════════════════════════════
    "Yoast SEO": {
        "category": "SEO",
        "icon": "https://cdn.simpleicons.org/yoast/A4286A",
        "html": [r"yoast\.com", r"yoast seo"],
    },
    "Rank Math": {
        "category": "SEO",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"rank-math", r"rankmath"],
    },
    "Schema.org": {
        "category": "SEO",
        "icon": "https://cdn.simpleicons.org/javascript/F7DF1E",
        "html": [r"schema\.org", r"application/ld\+json"],
    },

    # ═══════════════════════════════
    # PAIEMENT
    # ═══════════════════════════════
    "Stripe": {
        "category": "Paiement",
        "icon": "https://cdn.simpleicons.org/stripe/635BFF",
        "html": [r"js\.stripe\.com", r"stripe\.createToken"],
    },
    "PayPal": {
        "category": "Paiement",
        "icon": "https://cdn.simpleicons.org/paypal/003087",
        "html": [r"paypal\.com/sdk", r"paypalobjects\.com"],
    },
    "Klarna": {
        "category": "Paiement",
        "icon": "https://cdn.simpleicons.org/klarna/FFB3C7",
        "html": [r"klarna\.com", r"klarna-payments"],
    },
}


def extract_version(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match and match.lastindex:
            return match.group(1)
    return None


def scan_url(url):
    if not url.startswith("http"):
        url = "https://" + url

    result = {
        "url": url,
        "technologies": [],
        "headers": {},
        "error": None,
    }

    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (compatible; WappaScanner/1.0)"
        })
        html = response.text
        html_lower = html.lower()
        headers = {k.lower(): v for k, v in response.headers.items()}
        soup = BeautifulSoup(html, "html.parser")
        scripts = " ".join([s.get("src", "") for s in soup.find_all("script")])
        full_text = html + scripts

        result["headers"] = dict(response.headers)
        result["status_code"] = response.status_code

        for tech, sig in SIGNATURES.items():
            detected = False
            version = None

            for header_key, pattern in sig.get("headers", {}).items():
                header_val = headers.get(header_key, "")
                if header_val and re.search(pattern, header_val, re.I):
                    detected = True
                    v = extract_version(header_val, [pattern])
                    if v:
                        version = v

            for pattern in sig.get("html", []):
                if re.search(pattern, html_lower, re.I):
                    detected = True

            for pattern in sig.get("scripts", []):
                if re.search(pattern, scripts, re.I):
                    detected = True

            if detected and not version:
                version = extract_version(full_text, sig.get("version", []))

            if detected:
                result["technologies"].append({
                    "name": tech,
                    "category": sig.get("category", "Autre"),
                    "icon": sig.get("icon", ""),
                    "version": version,
                })

    except requests.exceptions.RequestException as e:
        result["error"] = str(e)

    return result