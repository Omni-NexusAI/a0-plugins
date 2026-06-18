import { createStore } from "/js/AlpineStore.js";
import { fetchApi } from "/js/api.js";

const model = {
    loading: false,
    sessions: [],
    stats: null,
    error: "",
    deleting: null,
    expanded: {},
    keepCount: 10,
    maxSizeMB: 50,
    lastActionResult: "",
    config: {
        enabled: true,
        auto_restore: true,
        auto_save: true,
    },
    configSaving: false,

    async init() {
        await this.loadConfig();
        await this.loadSessions();
    },

    async loadConfig() {
        try {
            const response = await fetchApi("/plugins/browser_session_sync/sessions_list", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "get_config" })
            });
            const data = await response.json();
            if (data.ok !== false && data.config) {
                this.config = {
                    enabled: Boolean(data.config.enabled),
                    auto_restore: Boolean(data.config.auto_restore),
                    auto_save: Boolean(data.config.auto_save),
                };
            }
        } catch (e) {
            this.error = e.message || "Failed to load settings";
        }
    },

    async saveConfig() {
        this.configSaving = true;
        this.error = "";
        try {
            const response = await fetchApi("/plugins/browser_session_sync/sessions_list", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "save_config", config: this.config })
            });
            const data = await response.json();
            if (data.ok !== false && data.config) {
                this.config = {
                    enabled: Boolean(data.config.enabled),
                    auto_restore: Boolean(data.config.auto_restore),
                    auto_save: Boolean(data.config.auto_save),
                };
                this.lastActionResult = "Settings saved";
            } else {
                this.error = data.error || "Failed to save settings";
            }
        } catch (e) {
            this.error = e.message || "Failed to save settings";
        } finally {
            this.configSaving = false;
        }
    },

    async loadSessions() {
        this.loading = true;
        this.error = "";
        try {
            const response = await fetchApi("/plugins/browser_session_sync/sessions_list", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "list" })
            });
            const data = await response.json();
            if (data.ok !== false) {
                this.sessions = data.sessions || [];
                this.stats = data.stats || null;
            } else {
                this.error = data.error || "Failed to load sessions";
            }
        } catch (e) {
            this.error = e.message || "Failed to load sessions";
        } finally {
            this.loading = false;
        }
    },

    async deleteSession(filename) {
        this.deleting = filename;
        try {
            const response = await fetchApi("/plugins/browser_session_sync/sessions_list", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "delete", filename })
            });
            const data = await response.json();
            if (data.ok !== false) {
                await this.loadSessions();
            }
        } catch (e) {
            console.error("Delete failed:", e);
        } finally {
            this.deleting = null;
        }
    },

    async deleteAll() {
        if (!confirm("Delete ALL saved browser sessions? This cannot be undone.")) return;
        this.deleting = "all";
        try {
            const response = await fetchApi("/plugins/browser_session_sync/sessions_list", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "delete_all" })
            });
            const data = await response.json();
            if (data.ok !== false) {
                this.lastActionResult = `Cleared ${data.deleted || 0} sessions`;
                await this.loadSessions();
            }
        } catch (e) {
            console.error("Clear all failed:", e);
        } finally {
            this.deleting = null;
        }
    },

    async pruneOldest() {
        this.loading = true;
        try {
            const response = await fetchApi("/plugins/browser_session_sync/sessions_list", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "prune", keep_count: this.keepCount })
            });
            const data = await response.json();
            if (data.ok !== false) {
                this.lastActionResult = data.message || `Pruned ${data.deleted} old sessions, kept latest ${this.keepCount}`;
                await this.loadSessions();
            }
        } catch (e) {
            console.error("Prune failed:", e);
        } finally {
            this.loading = false;
        }
    },

    async enforceMaxSize() {
        this.loading = true;
        try {
            const response = await fetchApi("/plugins/browser_session_sync/sessions_list", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "set_max_size", max_mb: this.maxSizeMB })
            });
            const data = await response.json();
            if (data.ok !== false) {
                this.lastActionResult = data.message || `Enforced max size: deleted ${data.deleted} sessions, freed ${data.freed || '0 B'}`;
                await this.loadSessions();
            }
        } catch (e) {
            console.error("Enforce max size failed:", e);
        } finally {
            this.loading = false;
        }
    },

    toggleDetails(name) {
        this.expanded[name] = !this.expanded[name];
    },

    getHostname(url) {
        if (!url) return "(empty)";
        try {
            return new URL(url).hostname;
        } catch {
            return url.substring(0, 50);
        }
    }
};

export const store = createStore("browserSessionSync", model);
