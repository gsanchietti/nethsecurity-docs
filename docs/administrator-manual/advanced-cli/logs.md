---
title: "Logs"
sidebar_position: 7
---

# Logs {#logs-section}

Logs are initially written to a temporary in-memory directory to prevent potential errors on the root file system in case of a failure.

1.  **Local Storage**: Logs can be written directly to storage. This can be configured from the UI, see the [Storage](../system/storage.md).
2.  **Remote Controller**: Logs can be automatically forwarded to a [remote controller](../system/controller.md#controller_logs-section).
3.  **Custom Syslog Forwarder**: Logs can be sent to a remote syslog server.
4.  **Cloud Log Manager**: Logs can be forwarded to the Nethesis Cloud Log Manager (CLM) service.

The next paragraphs will explain how to configure these latter options.

## Forwarding to a remote server

It is sufficient to configure the UCI database with the desired options, then commit the changes, and finally restart the service. Temporary logs will continue to be visible in `/var/log/messages` and will also be sent to the remote server.

Most syslog servers are configured to listen on UDP port 514 by default.

Example configuration for sending logs to the syslog server with IP 192.168.1.88 on UDP port 514. The configuration is named `clm` (custom log manager):

    uci set rsyslog.clm=forwarder
    uci set rsyslog.clm.source=*.* 
    uci set rsyslog.clm.protocol=udp
    uci set rsyslog.clm.port=514
    uci set rsyslog.clm.target=192.168.1.88

Once configured, simply commit the changes with the command: :

    uci commit rsyslog

And finally, restart the service: :

    /etc/init.d/rsyslog restart

By default the forwarder uses the TraditionalFileFormat (RFC 3164) for the logs. It is possible also to configure RFC 5424 using the same syntax: :

    uci set rsyslog.clm.rfc=5424

It is possible to configure multiple forwarders by repeating the operation using a different configuration name like `clm2`.

## Forwarding to Nethesis Cloud Log Manager

:::note

Service entitlement required

You need to purchase a subscription for the CLM service from Nethesis and obtain the tenant identifier. The service is currenlty reserved to Enterprise customers. For more information, please contact Nethesis sales.

:::

The `ns-clm` package forwards syslog messages to the Nethesis Cloud Log Manager (CLM) service. It provides the `ns-clm-forwarder` daemon, which tails `/var/log/messages` and tracks its read position in `/var/run/ns-clm/last_offset`. New syslog lines are parsed, batched, and sent as JSON via HTTP POST to the CLM endpoint. The daemon polls for new lines every 10 seconds, detects log rotation automatically, and persists the offset on shutdown so it can resume after a restart.

The package is not included by default on NethSecurity 8.7.2 or earlier, but it is available in the package repository and can be manually installed.

If you are running NethSecurity 8.8, use:

    apk update
    apk add ns-clm

If you are running NethSecurity 8.7.2 or older, use:

    opkg update
    opkg install ns-clm

The UCI configuration is stored in `/etc/config/ns-clm`:

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 30%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th>Option</th>
<th>Default</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>enabled</code></td>
<td><code>0</code></td>
<td>Enable (<code>1</code>) or disable (<code>0</code>) the forwarder</td>
</tr>
<tr>
<td><p><code>uuid</code></p></td>
<td><p>(empty)</p></td>
<td><p>Unique identifier for the device, generated with <code>uuidgen</code> and prefixed with "L" to ensure it starts with a letter.</p>
<p>This is required for the CLM service to identify the source of the logs.</p>
<p>Example: <code>L3d50ca11-4415-4e46-9ee9-b1da0f62c337</code></p></td>
</tr>
<tr>
<td><code>address</code></td>
<td><code>https://nar.nethesis.it</code></td>
<td>CLM server address</td>
</tr>
<tr>
<td><code>tenant</code></td>
<td>(empty)</td>
<td>CLM tenant identifier, available inside the CLM portal, under <code>Users and Companies</code> -&gt; <code>Companies</code></td>
</tr>
<tr>
<td><code>debug</code></td>
<td><code>0</code></td>
<td>Enable debug output to stderr (<code>1</code>)</td>
</tr>
</tbody>
</table>

To enable the forwarder and set the tenant identifier, run: :

    uci set ns-clm.config.uuid="L$(uuidgen)"
    uci set ns-clm.config.enabled=1
    uci set ns-clm.config.tenant=<tenant_id>
    uci commit ns-clm
    reload_config

You can find the tenant identifier in the CLM portal, under `Users and Companies` -\> `Companies`.

To also enable the service at boot: :

    /etc/init.d/ns-clm enable && /etc/init.d/ns-clm start

To stop and disable the forwarder: :

    /etc/init.d/ns-clm stop && /etc/init.d/ns-clm disable

## Log rotation {#log-rotation-section}

Logs are rotated to manage disk space and ensure that log files do not grow indefinitely.

### In-memory log rotation

The `/var/log/messages` log file is stored in RAM and it\'s rotated based on size. Once it reaches a predefined size limit, the log is rotated and compressed to conserve space. The rotated log is saved as `/var/log/messages.1.gz` in gzip format. The system retains only two versions of the log: the active log file and the latest rotated, compressed file. From version 1.4.0, by default, the log rotation threshold is set to 10% of the tmpfs filesystem mounted at `/tmp`.

The `ns-log-size` script manages the log rotation size for the Rsyslog service. It allows to **get** and **set** the log rotation size defined in bytes for the log file located at `/var/log/messages`.

- **Get current size**: Retrieve the current log rotation size in bytes.
- **Set new size**: Change the log rotation size to a specified value, ensuring that the new size is a positive integer and not less than 52428800 bytes (50 MB).
- **Configuration safety**: If the specified size is below the minimum threshold, the script warns the user and does not make any changes to the configuration.

#### Usage

To use the script, run it with the following syntax:

    ns-log-size {get|set <size>}

- **get**: Outputs the current log rotation size in bytes.
- **set \<size\>**: Sets the log rotation size to the specified value (in bytes).

##### Example

To get the current log rotation size:

    ns-log-size get

To set a new log rotation size to 104857600 bytes (100 MB):

    ns-log-size set 104857600

The service rsyslog is restarted automatically after the size is set.

All changes to the log rotation size are directly written in the Rsyslog configuration file `/etc/rsyslog.conf`.

### Storage log rotation {#storage-log-rotation-section}

When using persistent storage, log rotation is managed by the `logrotate` utility, which is configured to rotate logs weekly and keep a maximum of 52 weeks (1 year) of logs. After rotation, the logs are compressed using gzip and stored in the same directory with a naming convention that includes the date of rotation (e.g., `/mnt/data/log/messages-20260315.gz`).

The configuration file for logrotate is located at `/etc/logrotate.d/data.conf` and can be modified to change the rotation frequency and retention period as needed. The configuration file is automatically added to the backup and preserved during upgrades, so any custom settings persist.
