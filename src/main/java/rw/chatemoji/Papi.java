package rw.chatemoji;

import me.clip.placeholderapi.expansion.PlaceholderExpansion;
import org.bukkit.OfflinePlayer;

public final class Papi extends PlaceholderExpansion {
    private final RWChatEmoji pl;

    Papi(RWChatEmoji pl) {
        this.pl = pl;
    }

    @Override
    public String getIdentifier() {
        return "rwchatemoji";
    }

    @Override
    public String getAuthor() {
        return "RW";
    }

    @Override
    public String getVersion() {
        return "1.0";
    }

    @Override
    public boolean persist() {
        return true;
    }

    @Override
    public String onRequest(OfflinePlayer p, String id) {
        return pl.lookup(id.toLowerCase());
    }
}
