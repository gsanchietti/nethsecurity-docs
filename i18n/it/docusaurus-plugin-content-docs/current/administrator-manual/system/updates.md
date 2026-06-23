---
title: "Aggiornamenti"
sidebar_position: 4
---

# Aggiornamenti {#updates-section}

NethSecurity consente due tipi di aggiornamenti, entrambi disponibili dalla sezione `Aggiornamento` nel menu `Sistema`:

- aggiornamenti normali per correzioni di bug e patch di sicurezza
- aggiornamenti di sistema per passare a una versione diversa

## Correzioni di bug e sicurezza {#bug-security-fixes}

Questi aggiornamenti sono destinati a aggiornamenti minori e correzioni di bug.

Tipicamente potrebbero essere eseguiti automaticamente, ma in qualsiasi momento è possibile verificare la disponibilità di nuovi aggiornamenti facendo clic sul pulsante **Verifica correzioni**. Questi aggiornamenti non richiedono il riavvio di NethSecurity, sono legati a una versione specifica e distribuiti tramite pacchetti.

Quando si utilizza questo metodo, la versione dell'immagine mostrata nel dashboard non cambia, ma il sistema viene aggiornato con le ultime correzioni.

## Aggiornamenti di sistema {#system_upgrades-section}

Questi tipi di aggiornamenti comportano la transizione a una nuova versione del firmware che introduce nuove funzionalità, miglioramenti e un supporto hardware più ampio.

Questo tipo di aggiornamento riavvierà il dispositivo (che quindi non sarà raggiungibile per qualche decina di secondi) e poi riscriverà completamente il firmware, preservando tutte le configurazioni. Tuttavia, è consigliato salvare un backup della configurazione prima di procedere con l'aggiornamento.

Se una nuova versione è disponibile, l'interfaccia utente visualizzerà un banner informativo e un pulsante dedicato **Aggiorna sistema** che ti permetterà di eseguire l'aggiornamento.

In alternativa, è sempre possibile caricare manualmente un'immagine compatibile utilizzando il pulsante **Aggiorna con file immagine** e procedere con l'aggiornamento.

**Aggiornamento da riga di comando**

Puoi anche eseguire un `Aggiornamento di sistema` da riga di comando. Per farlo, scarica semplicemente il nuovo file immagine, è consigliato salvarlo nella directory `/tmp`. Quindi esegui il seguente comando: :

    sysupgrade -k -v nethsecurity-<version>-x86-64-generic-squashfs-combined.img.gz

Il comando `sysupgrade` scrive il nuovo file immagine sul dispositivo.

### Ripristinare pacchetti extra {#restore_extra_packages-section}

A partire dalla versione 8.7.2, i pacchetti extra vengono reinstallati automaticamente dopo l'aggiornamento di sistema. Si noti che la procedura di reinstallazione richiede accesso a Internet. Se uno o più pacchetti non possono essere installati perché la rete non è ancora pronta o si verifica un errore transitorio, il servizio di ripristino rimane abilitato e ritenta automaticamente al prossimo avvio fino a quando tutti i pacchetti non vengono ripristinati. I pacchetti ripristinati vengono riportati nel log. Ad esempio, un ripristino misto potrebbe registrare:

    Restored package: etherwake
    Failed to restore package: qemu-ga
    Some packages failed to restore, will retry later

In caso di errore, procedere con il ripristino manuale documentato di seguito. Vedi la sezione successiva per le versioni precedenti.

Dopo l'aggiornamento, puoi eseguire il seguente comando per elencare tutti i pacchetti extra: :

    grep overlay /etc/backup/installed_packages.txt

Questo comando restituisce tutti i pacchetti extra, permettendoti di verificare quali sono installati e presenti nel sistema.

#### Ripristinare manualmente i pacchetti extra

Questa procedura manuale è richiesta solo nelle versioni precedenti alla 8.7.2 o se la procedura di reinstallazione automatica non riesce.

Durante l'aggiornamento, il sistema viene completamente riscritto e tutti i pacchetti extra installati dall'utente andranno persi. Tuttavia, l'elenco dei pacchetti installati viene salvato nel backup della configurazione, permettendo di ripristinarli dopo l'aggiornamento.

Dopo l'aggiornamento, assicurati che il sistema abbia accesso a Internet, quindi ripristina i pacchetti precedentemente installati utilizzando i seguenti comandi: :

    opkg update
    grep -E '\w+\s+overlay$' /etc/backup/installed_packages.txt | awk '{print $1}' | xargs opkg install

## Aggiornamenti automatici dei pacchetti

:::note

Nessuna sottoscrizione richiesta

A partire da NethSecurity 8.8, questa funzionalità è disponibile anche senza una sottoscrizione.

:::

Gli aggiornamenti automatici per i pacchetti possono essere abilitati dalla sezione `Aggiornamento` nel menu `Sistema`, abilitando l'opzione `Aggiornamenti automatici`. Gli aggiornamenti vengono verificati quotidianamente e, se disponibili, vengono automaticamente scaricati e installati.

## Comandi di gestione pacchetti

NethSecurity 8.8 utilizza `apk`. NethSecurity 8.7.2 e versioni precedenti utilizzano `opkg`. Utilizzare il seguente riferimento rapido quando si traducono esempi di comandi più vecchi:

| Comando OPKG          | Equivalente APK      | Descrizione             |
|-----------------------|---------------------|-------------------------|
| `opkg install <pkg>`  | `apk add <pkg>`     | Installare un pacchetto       |
| `opkg remove <pkg>`   | `apk del <pkg>`     | Rimuovere un pacchetto        |
| `opkg upgrade`        | `apk upgrade`       | Aggiornare tutti i pacchetti    |
| `opkg files <pkg>`    | `apk info -L <pkg>` | Elencare il contenuto del pacchetto   |
| `opkg list-installed` | `apk info`          | Elencare i pacchetti installati |
| `opkg update`         | `apk update`        | Aggiornare gli elenchi dei pacchetti    |
| `opkg search <pkg>`   | `apk search <pkg>`  | Cercare pacchetti     |

Il comando `opkg find` utilizzato in pochi esempi precedenti è mappato su `apk search` in NethSecurity 8.8.
