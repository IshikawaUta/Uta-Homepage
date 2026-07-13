"""
Comprehensive tests for IshikawaUta Portfolio (uta-home).
Tests cover: routes, templates, error handlers, helpers, static files, and profile data.
Target: 95%+ code coverage.
"""

import json
import pytest
from app import app, PROFILE, build_jsonld


# =============================================================================
# Profile Data Tests
# =============================================================================

class TestProfileData:
    """Test PROFILE data structure and required fields."""

    def test_profile_is_dict(self):
        assert isinstance(PROFILE, dict)

    def test_profile_has_name(self):
        assert "name" in PROFILE
        assert isinstance(PROFILE["name"], str)
        assert len(PROFILE["name"]) > 0

    def test_profile_has_alias(self):
        assert "alias" in PROFILE
        assert isinstance(PROFILE["alias"], str)

    def test_profile_has_tagline(self):
        assert "tagline" in PROFILE
        assert isinstance(PROFILE["tagline"], str)

    def test_profile_has_code_file(self):
        assert "codeFile" in PROFILE
        assert PROFILE["codeFile"] == "app.py"

    def test_profile_has_avatar_url(self):
        assert "avatarUrl" in PROFILE
        assert PROFILE["avatarUrl"].startswith("https://")

    def test_profile_has_copyright(self):
        assert "copyright" in PROFILE
        assert isinstance(PROFILE["copyright"], str)

    def test_profile_has_about(self):
        assert "about" in PROFILE
        assert isinstance(PROFILE["about"], list)
        assert len(PROFILE["about"]) >= 1

    def test_profile_about_items_are_strings(self):
        for item in PROFILE["about"]:
            assert isinstance(item, str)
            assert len(item) > 0

    def test_profile_has_tags(self):
        assert "tags" in PROFILE
        assert isinstance(PROFILE["tags"], list)
        assert len(PROFILE["tags"]) >= 1

    def test_profile_tag_structure(self):
        for tag in PROFILE["tags"]:
            assert "year" in tag
            assert "label" in tag
            assert isinstance(tag["year"], str)
            assert isinstance(tag["label"], str)

    def test_profile_has_tech_stack(self):
        assert "techStack" in PROFILE
        assert "innerIcons" in PROFILE["techStack"]
        assert "outerIcons" in PROFILE["techStack"]
        assert isinstance(PROFILE["techStack"]["innerIcons"], list)
        assert isinstance(PROFILE["techStack"]["outerIcons"], list)

    def test_profile_has_social_links(self):
        assert "socialLinks" in PROFILE
        assert isinstance(PROFILE["socialLinks"], list)
        assert len(PROFILE["socialLinks"]) >= 1

    def test_profile_social_link_structure(self):
        for link in PROFILE["socialLinks"]:
            assert "label" in link
            assert "href" in link
            assert isinstance(link["label"], str)
            assert isinstance(link["href"], str)

    def test_profile_has_achievements(self):
        assert "achievements" in PROFILE
        assert isinstance(PROFILE["achievements"], list)
        assert len(PROFILE["achievements"]) >= 1

    def test_profile_achievement_structure(self):
        for ach in PROFILE["achievements"]:
            assert "title" in ach
            assert "description" in ach
            assert "year" in ach

    def test_profile_has_projects(self):
        assert "projects" in PROFILE
        assert isinstance(PROFILE["projects"], list)
        assert len(PROFILE["projects"]) >= 1

    def test_profile_project_structure(self):
        for project in PROFILE["projects"]:
            assert "title" in project
            assert "badges" in project
            assert "description" in project
            assert "github" in project
            assert isinstance(project["title"], str)
            assert isinstance(project["badges"], list)
            assert isinstance(project["description"], str)
            assert isinstance(project["github"], str)

    def test_profile_project_badge_structure(self):
        for project in PROFILE["projects"]:
            for badge in project["badges"]:
                assert "href" in badge
                assert "img" in badge
                assert "alt" in badge
                assert isinstance(badge["href"], str)
                assert isinstance(badge["img"], str)
                assert isinstance(badge["alt"], str)


# =============================================================================
# build_jsonld() Tests
# =============================================================================

class TestBuildJsonld:
    """Test JSON-LD structured data builder."""

    def test_returns_valid_json(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_has_context(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        assert data["@context"] == "https://schema.org"

    def test_has_profile_page_type(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        assert data["@type"] == "ProfilePage"

    def test_has_main_entity(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        assert "mainEntity" in data
        assert data["mainEntity"]["@type"] == "Person"

    def test_main_entity_name(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        assert data["mainEntity"]["name"] == PROFILE["name"]

    def test_main_entity_alternate_name(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        assert data["mainEntity"]["alternateName"] == PROFILE["alias"]

    def test_main_entity_url(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        assert data["mainEntity"]["url"] == sample_site_url

    def test_main_entity_same_as(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        assert isinstance(data["mainEntity"]["sameAs"], list)
        assert len(data["mainEntity"]["sameAs"]) == len(PROFILE["socialLinks"])

    def test_same_as_contains_social_urls(self, sample_site_url):
        result = build_jsonld(PROFILE, sample_site_url)
        data = json.loads(result)
        for link in PROFILE["socialLinks"]:
            assert link["href"] in data["mainEntity"]["sameAs"]


# =============================================================================
# Index Route Tests
# =============================================================================

class TestIndexRoute:
    """Test GET / route."""

    @pytest.mark.anyio
    async def test_index_returns_200(self, client):
        resp = await client.get("/")
        assert resp.status_code == 200

    @pytest.mark.anyio
    async def test_index_content_type_is_html(self, client):
        resp = await client.get("/")
        assert "text/html" in resp.headers.get("content-type", "")

    @pytest.mark.anyio
    async def test_index_contains_profile_name(self, client):
        resp = await client.get("/")
        assert PROFILE["name"].encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_alias(self, client):
        resp = await client.get("/")
        assert PROFILE["alias"].encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_tagline(self, client):
        resp = await client.get("/")
        assert PROFILE["tagline"].encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_canonical_url(self, client):
        resp = await client.get("/")
        assert b"<link rel=\"canonical\"" in resp.content

    @pytest.mark.anyio
    async def test_index_contains_json_ld(self, client):
        resp = await client.get("/")
        assert b"application/ld+json" in resp.content

    @pytest.mark.anyio
    async def test_index_json_ld_contains_profile_page(self, client):
        resp = await client.get("/")
        assert b"ProfilePage" in resp.content

    @pytest.mark.anyio
    async def test_index_contains_og_tags(self, client):
        resp = await client.get("/")
        assert b'og:type' in resp.content
        assert b'og:title' in resp.content
        assert b'og:description' in resp.content
        assert b'og:image' in resp.content
        assert b'og:url' in resp.content
        assert b'og:logo' in resp.content

    @pytest.mark.anyio
    async def test_index_contains_twitter_tags(self, client):
        resp = await client.get("/")
        assert b'twitter:card' in resp.content
        assert b'twitter:title' in resp.content
        assert b'twitter:description' in resp.content
        assert b'twitter:image' in resp.content

    @pytest.mark.anyio
    async def test_index_contains_tech_icons_script(self, client):
        resp = await client.get("/")
        assert b"window.__techIcons" in resp.content

    @pytest.mark.anyio
    async def test_index_contains_tech_stack_data(self, client):
        resp = await client.get("/")
        for icon in PROFILE["techStack"]["innerIcons"]:
            assert icon.encode() in resp.content
        for icon in PROFILE["techStack"]["outerIcons"]:
            assert icon.encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_social_links(self, client):
        resp = await client.get("/")
        for link in PROFILE["socialLinks"]:
            assert link["href"].encode() in resp.content
            assert link["label"].encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_achievements(self, client):
        resp = await client.get("/")
        for ach in PROFILE["achievements"]:
            assert ach["title"].encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_about_paragraphs(self, client):
        resp = await client.get("/")
        for paragraph in PROFILE["about"]:
            assert paragraph.encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_tags(self, client):
        resp = await client.get("/")
        for tag in PROFILE["tags"]:
            assert tag["label"].encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_projects_data(self, client):
        resp = await client.get("/")
        assert b"__projectsData" in resp.content

    @pytest.mark.anyio
    async def test_index_contains_project_titles(self, client):
        resp = await client.get("/")
        for project in PROFILE["projects"]:
            assert project["title"].encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_pagination_container(self, client):
        resp = await client.get("/")
        assert b"project-pagination" in resp.content

    @pytest.mark.anyio
    async def test_index_contains_pagination_script(self, client):
        resp = await client.get("/")
        assert b"pagination.js" in resp.content

    @pytest.mark.anyio
    async def test_index_contains_copyright(self, client):
        resp = await client.get("/")
        assert PROFILE["copyright"].encode() in resp.content

    @pytest.mark.anyio
    async def test_index_contains_theme_toggle(self, client):
        resp = await client.get("/")
        assert b"id=\"theme-toggle\"" in resp.content

    @pytest.mark.anyio
    async def test_index_contains_tech_circles(self, client):
        resp = await client.get("/")
        assert b"tech-circles-container" in resp.content
        assert b"inner-icons" in resp.content
        assert b"outer-icons" in resp.content

    @pytest.mark.anyio
    async def test_index_contains_code_preview(self, client):
        resp = await client.get("/")
        assert b"@dataclass" in resp.content
        assert b"Dev" in resp.content
        assert b"me = Dev()" in resp.content

    @pytest.mark.anyio
    async def test_index_with_forwarded_proto_https(self, client):
        resp = await client.get("/", headers={"x-forwarded-proto": "https"})
        assert resp.status_code == 200
        assert b"https://" in resp.content

    @pytest.mark.anyio
    async def test_index_with_custom_host(self, client):
        resp = await client.get("/", headers={"host": "example.com"})
        assert resp.status_code == 200
        assert b"example.com" in resp.content


# =============================================================================
# Favicon Route Tests
# =============================================================================

class TestFaviconRoute:
    """Test GET /favicon.ico route."""

    @pytest.mark.anyio
    async def test_favicon_returns_302(self, client):
        resp = await client.get("/favicon.ico")
        assert resp.status_code == 302

    @pytest.mark.anyio
    async def test_favicon_redirects_to_avatar(self, client):
        resp = await client.get("/favicon.ico")
        assert resp.headers.get("location") == PROFILE["avatarUrl"]

    @pytest.mark.anyio
    async def test_favicon_location_is_github_avatar(self, client):
        resp = await client.get("/favicon.ico")
        assert "avatars.githubusercontent.com" in resp.headers.get("location", "")


# =============================================================================
# Robots.txt Route Tests
# =============================================================================

class TestRobotsRoute:
    """Test GET /robots.txt route."""

    @pytest.mark.anyio
    async def test_robots_returns_200(self, client):
        resp = await client.get("/robots.txt")
        assert resp.status_code == 200

    @pytest.mark.anyio
    async def test_robots_content_type_is_text_plain(self, client):
        resp = await client.get("/robots.txt")
        assert "text/plain" in resp.headers.get("content-type", "")

    @pytest.mark.anyio
    async def test_robots_contains_user_agent(self, client):
        resp = await client.get("/robots.txt")
        assert b"User-agent: *" in resp.content

    @pytest.mark.anyio
    async def test_robots_contains_allow(self, client):
        resp = await client.get("/robots.txt")
        assert b"Allow: /" in resp.content

    @pytest.mark.anyio
    async def test_robots_contains_sitemap(self, client):
        resp = await client.get("/robots.txt")
        assert b"Sitemap:" in resp.content
        assert b"/sitemap.xml" in resp.content

    @pytest.mark.anyio
    async def test_robots_sitemap_url_with_default_host(self, client):
        resp = await client.get("/robots.txt")
        text = resp.text
        assert "http://test/sitemap.xml" in text

    @pytest.mark.anyio
    async def test_robots_with_forwarded_proto_https(self, client):
        resp = await client.get("/robots.txt", headers={"x-forwarded-proto": "https"})
        assert b"https://" in resp.content

    @pytest.mark.anyio
    async def test_robots_with_custom_host(self, client):
        resp = await client.get("/robots.txt", headers={"host": "example.com"})
        assert b"example.com" in resp.content


# =============================================================================
# Sitemap.xml Route Tests
# =============================================================================

class TestSitemapRoute:
    """Test GET /sitemap.xml route."""

    @pytest.mark.anyio
    async def test_sitemap_returns_200(self, client):
        resp = await client.get("/sitemap.xml")
        assert resp.status_code == 200

    @pytest.mark.anyio
    async def test_sitemap_content_type_is_xml(self, client):
        resp = await client.get("/sitemap.xml")
        assert "application/xml" in resp.headers.get("content-type", "")

    @pytest.mark.anyio
    async def test_sitemap_contains_xml_declaration(self, client):
        resp = await client.get("/")
        resp = await client.get("/sitemap.xml")
        assert b"<?xml version=\"1.0\"" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_contains_urlset(self, client):
        resp = await client.get("/sitemap.xml")
        assert b"<urlset" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_contains_url(self, client):
        resp = await client.get("/sitemap.xml")
        assert b"<url>" in resp.content
        assert b"</url>" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_contains_loc(self, client):
        resp = await client.get("/sitemap.xml")
        assert b"<loc>" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_contains_lastmod(self, client):
        resp = await client.get("/sitemap.xml")
        assert b"<lastmod>" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_contains_changefreq(self, client):
        resp = await client.get("/sitemap.xml")
        assert b"<changefreq>monthly</changefreq>" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_contains_priority(self, client):
        resp = await client.get("/sitemap.xml")
        assert b"<priority>1.0</priority>" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_url_with_default_host(self, client):
        resp = await client.get("/sitemap.xml")
        assert b"http://test/" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_with_forwarded_proto_https(self, client):
        resp = await client.get("/sitemap.xml", headers={"x-forwarded-proto": "https"})
        assert b"https://" in resp.content

    @pytest.mark.anyio
    async def test_sitemap_with_custom_host(self, client):
        resp = await client.get("/sitemap.xml", headers={"host": "example.com"})
        assert b"example.com" in resp.content


# =============================================================================
# Error Handler Tests
# =============================================================================

class TestErrorHandlers:
    """Test 404 and 500 error handlers."""

    @pytest.mark.anyio
    async def test_404_returns_404_status(self, client):
        resp = await client.get("/nonexistent-page")
        assert resp.status_code == 404

    @pytest.mark.anyio
    async def test_404_returns_html(self, client):
        resp = await client.get("/nonexistent-page")
        assert "text/html" in resp.headers.get("content-type", "")

    @pytest.mark.anyio
    async def test_404_contains_status_code(self, client):
        resp = await client.get("/nonexistent-page")
        assert b"404" in resp.content

    @pytest.mark.anyio
    async def test_404_contains_error_message(self, client):
        resp = await client.get("/nonexistent-page")
        assert b"Page not found" in resp.content

    @pytest.mark.anyio
    async def test_404_contains_back_home_link(self, client):
        resp = await client.get("/nonexistent-page")
        assert b"Back home" in resp.content
        assert b'href="/"' in resp.content

    @pytest.mark.anyio
    async def test_404_contains_profile_name(self, client):
        resp = await client.get("/nonexistent-page")
        assert PROFILE["name"].encode() in resp.content

    @pytest.mark.anyio
    async def test_500_returns_500_status(self, client):
        # We can't easily trigger a 500 from the outside,
        # but we can test the handler directly
        from app import server_error

        resp = await server_error(None, Exception("test"))
        # resp is a tuple (rendered_template, 500)
        assert resp[1] == 500

    @pytest.mark.anyio
    async def test_error_page_contains_profile(self, client):
        resp = await client.get("/nonexistent-page")
        assert PROFILE["avatarUrl"].encode() in resp.content


# =============================================================================
# Static Files Tests
# =============================================================================

class TestStaticFiles:
    """Test static file serving."""

    @pytest.mark.anyio
    async def test_css_returns_200(self, client):
        resp = await client.get("/static/css/style.css")
        assert resp.status_code == 200

    @pytest.mark.anyio
    async def test_css_content_type(self, client):
        resp = await client.get("/static/css/style.css")
        assert "text/css" in resp.headers.get("content-type", "")

    @pytest.mark.anyio
    async def test_css_contains_variables(self, client):
        resp = await client.get("/static/css/style.css")
        assert b"--background:" in resp.content
        assert b"--foreground:" in resp.content

    @pytest.mark.anyio
    async def test_theme_toggle_js_returns_200(self, client):
        resp = await client.get("/static/js/theme-toggle.js")
        assert resp.status_code == 200

    @pytest.mark.anyio
    async def test_theme_toggle_js_content_type(self, client):
        resp = await client.get("/static/js/theme-toggle.js")
        assert "javascript" in resp.headers.get("content-type", "")

    @pytest.mark.anyio
    async def test_theme_toggle_js_contains_storage_key(self, client):
        resp = await client.get("/static/js/theme-toggle.js")
        assert b"uta-color-mode" in resp.content

    @pytest.mark.anyio
    async def test_tech_circles_js_returns_200(self, client):
        resp = await client.get("/static/js/tech-circles.js")
        assert resp.status_code == 200

    @pytest.mark.anyio
    async def test_tech_circles_js_content_type(self, client):
        resp = await client.get("/static/js/tech-circles.js")
        assert "javascript" in resp.headers.get("content-type", "")

    @pytest.mark.anyio
    async def test_tech_circles_js_contains_config(self, client):
        resp = await client.get("/static/js/tech-circles.js")
        assert b"INNER_RADIUS" in resp.content
        assert b"OUTER_RADIUS" in resp.content
        assert b"DURATION" in resp.content

    @pytest.mark.anyio
    async def test_pagination_js_returns_200(self, client):
        resp = await client.get("/static/js/pagination.js")
        assert resp.status_code == 200

    @pytest.mark.anyio
    async def test_pagination_js_content_type(self, client):
        resp = await client.get("/static/js/pagination.js")
        assert "javascript" in resp.headers.get("content-type", "")

    @pytest.mark.anyio
    async def test_pagination_js_contains_init(self, client):
        resp = await client.get("/static/js/pagination.js")
        assert b"initProjectPagination" in resp.content


# =============================================================================
# Template Rendering Tests
# =============================================================================

class TestTemplates:
    """Test that templates render correctly."""

    @pytest.mark.anyio
    async def test_base_template_structure(self, client):
        resp = await client.get("/")
        content = resp.text
        assert "<!DOCTYPE html>" in content
        assert '<html lang="en">' in content
        assert "<head>" in content
        assert "<body" in content
        assert "</html>" in content

    @pytest.mark.anyio
    async def test_base_template_meta_tags(self, client):
        resp = await client.get("/")
        content = resp.text
        assert '<meta charset="utf-8">' in content
        assert 'name="viewport"' in content
        assert 'name="description"' in content
        assert 'name="theme-color"' in content
        assert 'name="author"' in content
        assert 'name="keywords"' in content

    @pytest.mark.anyio
    async def test_base_template_fonts(self, client):
        resp = await client.get("/")
        content = resp.text
        assert "fonts.googleapis.com" in content
        assert "Inter" in content
        assert "Geist+Mono" in content

    @pytest.mark.anyio
    async def test_base_template_tailwind(self, client):
        resp = await client.get("/")
        content = resp.text
        assert "cdn.tailwindcss.com" in content
        assert "tailwind.config" in content

    @pytest.mark.anyio
    async def test_base_template_scripts(self, client):
        resp = await client.get("/")
        content = resp.text
        assert "theme-toggle.js" in content
        assert "tech-circles.js" in content

    @pytest.mark.anyio
    async def test_base_template_favicon(self, client):
        resp = await client.get("/")
        content = resp.text
        assert 'rel="icon"' in content
        assert PROFILE["avatarUrl"] in content

    @pytest.mark.anyio
    async def test_base_template_foUC_script(self, client):
        resp = await client.get("/")
        content = resp.text
        assert "uta-color-mode" in content

    @pytest.mark.anyio
    async def test_index_template_sections(self, client):
        resp = await client.get("/")
        content = resp.text
        assert "About &amp; Tech" in content or "About & Tech" in content
        assert "Project Experience" in content
        assert "Achievements" in content
        assert "Tech Stack" in content

    @pytest.mark.anyio
    async def test_index_template_header(self, client):
        resp = await client.get("/")
        content = resp.text
        assert "<h1" in content
        assert PROFILE["name"] in content
        assert PROFILE["alias"] in content

    @pytest.mark.anyio
    async def test_index_template_footer(self, client):
        resp = await client.get("/")
        content = resp.text
        assert "<footer" in content
        assert PROFILE["copyright"] in content

    @pytest.mark.anyio
    async def test_error_template_renders(self, client):
        resp = await client.get("/nonexistent-page")
        content = resp.text
        assert "<!DOCTYPE html>" in content
        assert "404" in content
        assert "Page not found" in content


# =============================================================================
# App Configuration Tests
# =============================================================================

class TestAppConfig:
    """Test app configuration and setup."""

    def test_app_title(self):
        assert app.title == "IshikawaUta Portfolio"

    def test_app_version(self):
        assert app.version == "1.0.0"

    def test_app_has_router(self):
        assert hasattr(app, "router")

    def test_app_has_exception_handlers(self):
        assert hasattr(app, "exception_handlers")
        assert 404 in app.exception_handlers
        assert 500 in app.exception_handlers

    def test_app_has_middleware(self):
        assert hasattr(app, "_asgi_middlewares") or hasattr(app, "middleware_stack")


# =============================================================================
# JSON-LD Rendering Tests
# =============================================================================

class TestJsonLdRendering:
    """Test JSON-LD is properly rendered in HTML."""

    @pytest.mark.anyio
    async def test_json_ld_script_tag(self, client):
        resp = await client.get("/")
        assert b'<script type="application/ld+json">' in resp.content

    @pytest.mark.anyio
    async def test_json_ld_closes_script_tag(self, client):
        resp = await client.get("/")
        assert b'</script>' in resp.content

    @pytest.mark.anyio
    async def test_json_ld_contains_schema_context(self, client):
        resp = await client.get("/")
        assert b'"@context": "https://schema.org"' in resp.content

    @pytest.mark.anyio
    async def test_json_ld_contains_person_type(self, client):
        resp = await client.get("/")
        assert b'"@type": "Person"' in resp.content

    @pytest.mark.anyio
    async def test_json_ld_contains_same_as(self, client):
        resp = await client.get("/")
        assert b'"sameAs"' in resp.content


# =============================================================================
# Canonical URL Tests
# =============================================================================

class TestCanonicalUrl:
    """Test canonical URL is dynamic."""

    @pytest.mark.anyio
    async def test_canonical_url_in_head(self, client):
        resp = await client.get("/")
        assert b'<link rel="canonical"' in resp.content

    @pytest.mark.anyio
    async def test_canonical_url_default(self, client):
        resp = await client.get("/")
        assert b"http://test/" in resp.content

    @pytest.mark.anyio
    async def test_canonical_url_with_forwarded_proto(self, client):
        resp = await client.get("/", headers={"x-forwarded-proto": "https"})
        assert b"https://test/" in resp.content

    @pytest.mark.anyio
    async def test_canonical_url_with_custom_host(self, client):
        resp = await client.get("/", headers={"host": "mysite.com"})
        assert b"http://mysite.com/" in resp.content


# =============================================================================
# View Transitions CSS Tests
# =============================================================================

class TestViewTransitionsCSS:
    """Test View Transitions API CSS is present."""

    @pytest.mark.anyio
    async def test_css_contains_view_transitions(self, client):
        resp = await client.get("/static/css/style.css")
        assert b"view-transition-old" in resp.content
        assert b"view-transition-new" in resp.content

    @pytest.mark.anyio
    async def test_css_contains_dark_mode_variables(self, client):
        resp = await client.get("/static/css/style.css")
        assert b".dark" in resp.content

    @pytest.mark.anyio
    async def test_css_contains_orbit_keyframes(self, client):
        resp = await client.get("/static/css/style.css")
        assert b"@keyframes orbit" in resp.content

    @pytest.mark.anyio
    async def test_css_contains_gradient_spin_keyframes(self, client):
        resp = await client.get("/static/css/style.css")
        assert b"@keyframes gradient-spin" in resp.content

    @pytest.mark.anyio
    async def test_css_contains_pagination_styles(self, client):
        resp = await client.get("/static/css/style.css")
        assert b"pagination-nav" in resp.content
        assert b"pagination-btn" in resp.content
        assert b"pagination-dot" in resp.content
        assert b"project-page" in resp.content
