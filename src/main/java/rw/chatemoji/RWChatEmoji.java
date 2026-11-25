package rw.chatemoji;

import io.papermc.paper.event.player.AsyncChatEvent;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.PatternReplacementResult;
import net.kyori.adventure.text.TextReplacementConfig;
import net.kyori.adventure.text.event.ClickEvent;
import net.kyori.adventure.text.event.HoverEvent;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.minimessage.MiniMessage;
import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabExecutor;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.entity.Player;
import org.bukkit.event.block.SignChangeEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.*;
import java.util.regex.Pattern;

public final class RWChatEmoji extends JavaPlugin implements Listener, TabExecutor {
    private static final MiniMessage MM = MiniMessage.miniMessage();
    private static final Pattern TOKEN = Pattern.compile(":([a-z0-9_]+):");
    private final Map<String, Component> emojis = new TreeMap<>();
    private final UUID packId = UUID.nameUUIDFromBytes("rwchatemoji-pack".getBytes());
    private volatile byte[] hash;
    private String url = "";

    @Override
    public void onEnable() {
        saveDefaultConfig();
        load();
        fetchHash();
        getServer().getPluginManager().registerEvents(this, this);
        getCommand("rwchatemoji").setExecutor(this);
        getCommand("rwchatemoji").setTabCompleter(this);
        getLogger().info("RWChatEmoji loaded " + emojis.size() + " shortcodes.");
    }

    private void load() {
        reloadConfig();
        emojis.clear();
        ConfigurationSection sec = getConfig().getConfigurationSection("emojis");
        if (sec == null) return;
        for (String key : sec.getKeys(false)) {
            String raw = sec.getString(key);
            if (raw == null || raw.isBlank()) continue;
            try {
                emojis.put(key.toLowerCase(Locale.ROOT), MM.deserialize(raw));
            } catch (RuntimeException ex) {
                getLogger().warning("Bad emoji '" + key + "': " + ex.getMessage());
            }
        }
    }

    private void fetchHash() {
        url = getConfig().getString("pack.url", "");
        hash = null;
        if (!getConfig().getBoolean("pack.enabled", true) || url.isBlank()) return;
        final String hu = url.replace(".zip", ".sha1");
        Bukkit.getScheduler().runTaskAsynchronously(this, () -> {
            try (var in = new java.net.URI(hu).toURL().openStream()) {
                String hex = new String(in.readAllBytes(), java.nio.charset.StandardCharsets.UTF_8).trim();
                if (hex.length() >= 40) {
                    byte[] b = new byte[20];
                    for (int i = 0; i < 20; i++) b[i] = (byte) Integer.parseInt(hex.substring(i * 2, i * 2 + 2), 16);
                    hash = b;
                }
            } catch (Exception ex) {
                getLogger().warning("Could not read pack hash: " + ex.getMessage());
            }
        });
    }

    private void sendPack(Player p) {
        if (url.isBlank() || !getConfig().getBoolean("pack.enabled", true)) return;
        p.setResourcePack(packId, url, hash, Component.text("RWChatEmoji emoji pack"), false);
    }

    @EventHandler
    public void onJoin(PlayerJoinEvent e) {
        Bukkit.getScheduler().runTaskLater(this, () -> sendPack(e.getPlayer()), 40L);
    }

    private Component parse(Component in) {
        return in.replaceText(TextReplacementConfig.builder()
                .match(TOKEN)
                .condition((m, count, replaced) -> emojis.containsKey(m.group(1))
                        ? PatternReplacementResult.REPLACE : PatternReplacementResult.CONTINUE)
                .replacement((m, b) -> emojis.get(m.group(1)))
                .build());
    }

    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onChat(AsyncChatEvent e) {
        if (!getConfig().getBoolean("chat", true) || !e.getPlayer().hasPermission("rwchatemoji.use")) return;
        e.message(parse(e.message()));
    }

    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onSign(SignChangeEvent e) {
        if (!getConfig().getBoolean("signs", true) || !e.getPlayer().hasPermission("rwchatemoji.use")) return;
        for (int i = 0; i < 4; i++) {
            Component line = e.line(i);
            if (line != null) e.line(i, parse(line));
        }
    }

    @Override
    public boolean onCommand(CommandSender s, Command cmd, String label, String[] a) {
        String sub = a.length == 0 ? "list" : a[0].toLowerCase(Locale.ROOT);
        if (sub.equals("reload")) {
            if (!s.hasPermission("rwchatemoji.admin")) {
                s.sendMessage(Component.text("No permission.", NamedTextColor.RED));
                return true;
            }
            load();
            fetchHash();
            s.sendMessage(Component.text("[RWChatEmoji] Reloaded " + emojis.size() + " shortcodes.", NamedTextColor.GREEN));
            return true;
        }
        if (sub.equals("pack")) {
            if (s instanceof Player p) sendPack(p);
            return true;
        }
        s.sendMessage(Component.text("[RWChatEmoji] Type the code in chat or on a sign. Click one to copy:", NamedTextColor.GOLD));
        for (Map.Entry<String, Component> en : emojis.entrySet()) {
            String code = ":" + en.getKey() + ":";
            s.sendMessage(Component.text("  " + code + "  ", NamedTextColor.YELLOW)
                    .append(en.getValue())
                    .clickEvent(ClickEvent.copyToClipboard(code))
                    .hoverEvent(HoverEvent.showText(Component.text("Click to copy " + code, NamedTextColor.GRAY))));
        }
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender s, Command c, String l, String[] a) {
        if (a.length == 1) {
            List<String> r = new ArrayList<>(List.of("list", "pack"));
            if (s.hasPermission("rwchatemoji.admin")) r.add("reload");
            r.removeIf(x -> !x.startsWith(a[0].toLowerCase(Locale.ROOT)));
            return r;
        }
        return List.of();
    }
  }
