---
title: "Backup e ripristino"
sidebar_position: 3
---

# Backup e ripristino

NethSecurity fornisce un sistema di backup flessibile e potente per salvare e ripristinare le impostazioni di configurazione del firewall.

Accedi alla pagina `Backup & Restore` nella sezione `System`, quindi fai clic sul pulsante **Download backup**. Se la macchina ha un abbonamento Enterprise valido, il backup è [automatico](#automatic_backup-section).

Il backup include tutti i file di configurazione rilevanti e anche l'elenco dei pacchetti extra installati dall'utente. L'elenco è salvato nel file `/etc/backup/installed_packages.txt`.

## Backup

NethSecurity consente la creazione di backup sia crittografati che non crittografati. Il download di un backup non crittografato è sempre possibile facendo clic sul pulsante **Download unencrypted**.

Per consentire il download di un backup crittografato, fai prima clic sul pulsante **Configure passphrase** e imposta una password forte. Dopo di ciò, il pulsante **Download encrypted** diventerà attivo.

:::note

Se il backup è crittografato e la password viene persa, non sarà più possibile ripristinare la configurazione.

:::

Per disabilitare i backup crittografati, fai clic sul pulsante **Remove passphrase** e il pulsante **Download encrypted** diventerà inattivo.

## Ripristino {#automatic_backup-section}

Il backup può essere ripristinato dalla scheda `Restore` all'interno della pagina `Backup & Restore`. L'utente può avviare il processo di ripristino facendo clic sul pulsante **Restore backup** e caricando il file di backup. Se la macchina ha un abbonamento Enterprise valido, l'interfaccia web presenterà inoltre un elenco dei backup disponibili dal server remoto. Se il backup è crittografato, inserisci la passphrase e infine fai clic sul pulsante **Restore** per completare il processo.

Dopo il ripristino il sistema verrà riavviato.

:::note

A partire dalla versione 8.7.2, i pacchetti extra vengono reinstallati automaticamente dopo l'aggiornamento del sistema. Per le versioni precedenti e per ulteriori informazioni, consulta questa documentazione: [Restore extra packages](./updates.md#restore_extra_packages-section).

:::

## Macchine con abbonamento

:::note

Abbonamento richiesto

Questa funzione è disponibile solo se il firewall ha un abbonamento valido.

:::

I backup si comportano diversamente su dispositivi con un [abbonamento](./subscription.md) attivo.

I backup non crittografati possono ancora essere scaricati direttamente dall'interfaccia utente di NethSecurity facendo clic sul pulsante **Download unencrypted**.

I backup crittografati sono archiviati nel cloud e integrati con Nethesis Operation Center: questo approccio semplifica la gestione dei backup e il processo di ripristino per i dispositivi basati su abbonamento, che possono interagire direttamente con Operation Center e scaricare automaticamente il backup durante il ripristino.

Per abilitare i backup cloud crittografati, è necessario configurare prima una passphrase facendo clic sul pulsante **Configure passphrase** e impostando una password forte. Una volta impostata la passphrase, puoi:

- Fare clic sul pulsante **Run cloud backup** per creare un backup immediatamente
- Consentire al sistema di creare automaticamente un backup ogni notte

Ogni backup crittografato verrà inviato direttamente a Nethesis Operation Center su un canale sicuro. Si prega di notare che la data del backup è la data del server. Le date visualizzate nell'elenco dei backup si basano sull'ora del server che archivia i backup, non sull'ora del firewall che li ha creati. Ciò significa che le date potrebbero differire a seconda delle differenze di fuso orario.

:::warning

I backup cloud senza crittografia sono stati deprecati. Per un tempo limitato, i backup verranno ancora inviati al cloud anche se non sono crittografati. Nel prossimo futuro, solo i backup crittografati verranno inviati al server remoto. Se hai un abbonamento valido, abilita la crittografia per garantire la sicurezza del tuo backup. Vedi anche [Avviso di crittografia del backup](#backup_encryption-alert) per ulteriori informazioni.

:::

### Avviso di crittografia del backup {#backup_encryption-alert}

Non crittografare il backup è un rischio per la sicurezza. Se il backup non è crittografato, chiunque abbia accesso al file di backup può leggere le impostazioni di configurazione archiviate al suo interno.

Ogni notte uno script verificherà se il backup è crittografato. Se il backup non è crittografato, lo script creerà un avviso all'interno del portale remoto my.nethesis.it o my.nethserver.com. Per risolvere l'avviso, l'utente deve abilitare la crittografia facendo clic sul pulsante **Configure passphrase** e impostando una password forte. L'avviso verrà risolto automaticamente durante il processo cron notturno.

Per disabilitare l'avviso, accedi alla shell ed esegui:

    uci set ns-plug.config.backup_alert_disabled=1
    uci commit ns-plug

La disabilitazione dell'avviso comporterà errori silenziosi quando l'invio di backup non crittografati verrà bloccato in futuro. L'amministratore non verrà notificato di questi errori, il che potrebbe portare a problemi di backup non notati.

## Personalizzazione del backup

Il backup include tutti i file di configurazione rilevanti. Per elencare i file inclusi nel backup, esegui il seguente comando:

    sysupgrade -l

Il backup può essere personalizzato aggiungendo file all'elenco dei backup. Aggiungi una nuova riga al file `/etc/sysupgrade.conf` con il percorso del file da includere nel backup.

Esempio:

    echo /etc/myfile >> /etc/sysupgrade.conf

## Come decrittografare un backup

Normalmente, i backup crittografati vengono gestiti direttamente da NethSecurity sia durante la creazione che durante le fasi di ripristino. Una volta fornita la passphrase, il sistema crittografa o decrittografa automaticamente il file.

In alcuni casi, però, può essere utile decrittografare il backup esternamente (al di fuori del firewall) per eseguire verifiche prima di ripristinarlo. Per questo motivo, è possibile utilizzare il seguente comando `gpg` per decrittografare il contenuto del backup:

    gpg --decrypt --passphrase $YOUR_PASSPHRASE --output unencrypted-file.tar.gz --yes $YOUR_ENCRYPTED_BACKUP_FILE
