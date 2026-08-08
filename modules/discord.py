import requests
import json
import time
import random
import string
from datetime import datetime

def get_token():
    return input("  >> Enter your Discord bot token: ").strip()

def get_guild_id():
    return input("  >> Enter guild (server) ID: ").strip()

def get_channel_id():
    return input("  >> Enter channel ID: ").strip()

def print_success(text):
    print(f"  >> {text}")

def print_error(text):
    print(f"  >> {text}")

def print_info(text):
    print(f"  >> {text}")

def discord_api_request(endpoint, token, method='GET', json_data=None, params=None):
    url = f'https://discord.com/api/v10/{endpoint}'
    headers = {'Authorization': f'Bot {token}', 'Content-Type': 'application/json'}
    try:
        if method == 'GET':
            r = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == 'POST':
            r = requests.post(url, headers=headers, json=json_data, timeout=10)
        elif method == 'PUT':
            r = requests.put(url, headers=headers, json=json_data, timeout=10)
        elif method == 'DELETE':
            r = requests.delete(url, headers=headers, timeout=10)
        elif method == 'PATCH':
            r = requests.patch(url, headers=headers, json=json_data, timeout=10)
        else:
            return None, "Invalid method"
        return r, None
    except Exception as e:
        return None, str(e)

def webhook_spammer(*args):
    if not args:
        url = input("  >> Webhook URL: ").strip()
        message = input("  >> Message to send: ").strip()
        count = input("  >> Number of messages: ").strip()
    else:
        url, message, count = args[0], args[1], args[2]
    try:
        count = int(count)
    except ValueError:
        print_error("Count must be a number.")
        return
    for i in range(count):
        try:
            r = requests.post(url, json={"content": message})
            if r.status_code == 204:
                print_success(f"Sent message {i+1}/{count}")
            else:
                print_error(f"Failed: {r.status_code}")
        except Exception as e:
            print_error(f"Error: {e}")
        time.sleep(0.5)

def mass_ban(*args):
    token = get_token()
    guild_id = get_guild_id()
    user_ids = input("  >> Enter user IDs separated by space: ").strip().split()
    if not user_ids:
        print_error("No user IDs provided.")
        return
    headers = {"Authorization": f"Bot {token}"}
    for uid in user_ids:
        url = f"https://discord.com/api/v10/guilds/{guild_id}/bans/{uid}"
        r = requests.put(url, headers=headers)
        if r.status_code in (204, 201):
            print_success(f"Banned {uid}")
        else:
            print_error(f"Failed to ban {uid}: {r.status_code}")

def mass_kick(*args):
    token = get_token()
    guild_id = get_guild_id()
    user_ids = input("  >> Enter user IDs separated by space: ").strip().split()
    if not user_ids:
        print_error("No user IDs provided.")
        return
    headers = {"Authorization": f"Bot {token}"}
    for uid in user_ids:
        url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{uid}"
        r = requests.delete(url, headers=headers)
        if r.status_code == 204:
            print_success(f"Kicked {uid}")
        else:
            print_error(f"Failed to kick {uid}: {r.status_code}")

def server_backup(*args):
    token = get_token()
    guild_id = get_guild_id()
    headers = {"Authorization": f"Bot {token}"}
    data = {}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers)
    if r.status_code == 200:
        data['channels'] = r.json()
    else:
        print_error(f"Failed to get channels: {r.status_code}")
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers)
    if r.status_code == 200:
        data['roles'] = r.json()
    else:
        print_error(f"Failed to get roles: {r.status_code}")
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers=headers)
    if r.status_code == 200:
        data['guild'] = r.json()
    else:
        print_error(f"Failed to get guild info: {r.status_code}")
    if data:
        with open(f"backup_{guild_id}.json", "w") as f:
            json.dump(data, f, indent=2)
        print_success(f"Backup saved to backup_{guild_id}.json")
    else:
        print_error("No data to backup.")

def mass_channel_delete(*args):
    token = get_token()
    guild_id = get_guild_id()
    confirm = input("  >> Are you sure? This will delete ALL channels! Type 'yes' to continue: ").strip().lower()
    if confirm != "yes":
        print_info("Aborted.")
        return
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers)
    if r.status_code != 200:
        print_error(f"Failed to fetch channels: {r.status_code}")
        return
    channels = r.json()
    for ch in channels:
        url = f"https://discord.com/api/v10/channels/{ch['id']}"
        r = requests.delete(url, headers=headers)
        if r.status_code == 200:
            print_success(f"Deleted channel {ch['name']} ({ch['id']})")
        else:
            print_error(f"Failed to delete {ch['name']}: {r.status_code}")

def mass_role_delete(*args):
    token = get_token()
    guild_id = get_guild_id()
    confirm = input("  >> Are you sure? This will delete ALL roles! Type 'yes' to continue: ").strip().lower()
    if confirm != "yes":
        print_info("Aborted.")
        return
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers)
    if r.status_code != 200:
        print_error(f"Failed to fetch roles: {r.status_code}")
        return
    roles = r.json()
    for role in roles:
        if role['name'] == '@everyone':
            continue
        url = f"https://discord.com/api/v10/guilds/{guild_id}/roles/{role['id']}"
        r = requests.delete(url, headers=headers)
        if r.status_code == 204:
            print_success(f"Deleted role {role['name']} ({role['id']})")
        else:
            print_error(f"Failed to delete {role['name']}: {r.status_code}")

def server_info(*args):
    token = get_token()
    guild_id = get_guild_id()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers=headers, params={'with_counts': 'true'})
    if r.status_code == 200:
        data = r.json()
        print_info(f"Server: {data.get('name')}")
        print_info(f"ID: {data.get('id')}")
        print_info(f"Owner ID: {data.get('owner_id')}")
        print_info(f"Members: {data.get('approximate_member_count', 'N/A')}")
        print_info(f"Boosts: {data.get('premium_subscription_count', 0)}")
        print_info(f"Boost Level: {data.get('premium_tier', 0)}")
        print_info(f"Channels: {len(data.get('channels', []))}")
        print_info(f"Roles: {len(data.get('roles', []))}")
        print_info(f"Verification Level: {data.get('verification_level', 'N/A')}")
    else:
        print_error(f"Failed to get server info: {r.status_code}")

def create_invite(*args):
    token = get_token()
    channel_id = get_channel_id()
    headers = {"Authorization": f"Bot {token}"}
    max_age = input("  >> Max age in seconds (default 86400): ").strip()
    max_age = int(max_age) if max_age else 86400
    max_uses = input("  >> Max uses (default 0 = unlimited): ").strip()
    max_uses = int(max_uses) if max_uses else 0
    data = {"max_age": max_age, "max_uses": max_uses, "temporary": False, "unique": True}
    r = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/invites", headers=headers, json=data)
    if r.status_code == 200:
        invite = r.json()
        print_success(f"Invite created: https://discord.gg/{invite.get('code')}")
        print_info(f"Max Age: {max_age}s")
        print_info(f"Max Uses: {max_uses if max_uses else 'unlimited'}")
    else:
        print_error(f"Failed to create invite: {r.status_code}")

def prune_members(*args):
    token = get_token()
    guild_id = get_guild_id()
    days = input("  >> Number of days inactive (1-30): ").strip()
    try:
        days = int(days)
        if days < 1 or days > 30:
            print_error("Days must be between 1 and 30")
            return
    except:
        print_error("Invalid number")
        return
    headers = {"Authorization": f"Bot {token}"}
    r = requests.post(f"https://discord.com/api/v10/guilds/{guild_id}/prune", headers=headers, json={"days": days})
    if r.status_code == 200:
        data = r.json()
        print_success(f"Pruned {data.get('pruned', 0)} members")
    else:
        print_error(f"Failed to prune: {r.status_code}")

def list_channels(*args):
    token = get_token()
    guild_id = get_guild_id()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers)
    if r.status_code == 200:
        channels = r.json()
        for ch in channels:
            ch_type = {0: "Text", 2: "Voice", 4: "Category", 13: "Stage"}.get(ch.get('type'), "Unknown")
            print_info(f"{ch.get('name')} ({ch_type}) - ID: {ch.get('id')}")
    else:
        print_error(f"Failed to list channels: {r.status_code}")

def list_roles(*args):
    token = get_token()
    guild_id = get_guild_id()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers)
    if r.status_code == 200:
        roles = r.json()
        for role in roles:
            print_info(f"{role.get('name')} - ID: {role.get('id')} - Color: {role.get('color')}")
    else:
        print_error(f"Failed to list roles: {r.status_code}")

def delete_all_webhooks(*args):
    token = get_token()
    guild_id = get_guild_id()
    confirm = input("  >> Are you sure? This will delete ALL webhooks! Type 'yes' to continue: ").strip().lower()
    if confirm != "yes":
        print_info("Aborted.")
        return
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/webhooks", headers=headers)
    if r.status_code != 200:
        print_error(f"Failed to fetch webhooks: {r.status_code}")
        return
    webhooks = r.json()
    for webhook in webhooks:
        r = requests.delete(f"https://discord.com/api/v10/webhooks/{webhook['id']}", headers=headers)
        if r.status_code == 204:
            print_success(f"Deleted webhook {webhook.get('name')}")
        else:
            print_error(f"Failed to delete webhook {webhook.get('name')}: {r.status_code}")

def get_user_info(*args):
    token = get_token()
    user_id = input("  >> Enter user ID: ").strip()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/users/{user_id}", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print_info(f"Username: {data.get('username')}#{data.get('discriminator', '0')}")
        print_info(f"ID: {data.get('id')}")
        print_info(f"Bot: {data.get('bot', False)}")
        print_info(f"Verified: {data.get('verified', False)}")
        print_info(f"Created: {data.get('created_at', 'N/A')}")
    else:
        print_error(f"Failed to get user info: {r.status_code}")

def get_member_info(*args):
    token = get_token()
    guild_id = get_guild_id()
    user_id = input("  >> Enter user ID: ").strip()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}", headers=headers)
    if r.status_code == 200:
        data = r.json()
        user = data.get('user', {})
        print_info(f"Username: {user.get('username')}#{user.get('discriminator', '0')}")
        print_info(f"Joined: {data.get('joined_at')}")
        print_info(f"Roles: {len(data.get('roles', []))}")
        print_info(f"Nickname: {data.get('nick', 'None')}")
    else:
        print_error(f"Failed to get member info: {r.status_code}")

def list_emojis(*args):
    token = get_token()
    guild_id = get_guild_id()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/emojis", headers=headers)
    if r.status_code == 200:
        emojis = r.json()
        for emoji in emojis:
            print_info(f"{emoji.get('name')} - ID: {emoji.get('id')}")
    else:
        print_error(f"Failed to list emojis: {r.status_code}")

def delete_emoji(*args):
    token = get_token()
    guild_id = get_guild_id()
    emoji_id = input("  >> Enter emoji ID: ").strip()
    confirm = input("  >> Delete this emoji? (y/n): ").strip().lower()
    if confirm != 'y':
        print_info("Aborted")
        return
    headers = {"Authorization": f"Bot {token}"}
    r = requests.delete(f"https://discord.com/api/v10/guilds/{guild_id}/emojis/{emoji_id}", headers=headers)
    if r.status_code == 204:
        print_success("Emoji deleted")
    else:
        print_error(f"Failed to delete emoji: {r.status_code}")

def create_channel(*args):
    token = get_token()
    guild_id = get_guild_id()
    name = input("  >> Channel name: ").strip()
    ch_type = input("  >> Type (text/voice): ").strip().lower()
    ch_type_id = 0 if ch_type == 'text' else 2
    headers = {"Authorization": f"Bot {token}"}
    data = {"name": name, "type": ch_type_id}
    r = requests.post(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers, json=data)
    if r.status_code == 200:
        print_success(f"Created channel: {name}")
    else:
        print_error(f"Failed to create channel: {r.status_code}")

def create_role(*args):
    token = get_token()
    guild_id = get_guild_id()
    name = input("  >> Role name: ").strip()
    headers = {"Authorization": f"Bot {token}"}
    data = {"name": name}
    r = requests.post(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers, json=data)
    if r.status_code == 200:
        print_success(f"Created role: {name}")
    else:
        print_error(f"Failed to create role: {r.status_code}")

def modify_channel(*args):
    token = get_token()
    channel_id = get_channel_id()
    name = input("  >> New channel name: ").strip()
    headers = {"Authorization": f"Bot {token}"}
    data = {"name": name}
    r = requests.patch(f"https://discord.com/api/v10/channels/{channel_id}", headers=headers, json=data)
    if r.status_code == 200:
        print_success(f"Channel modified: {name}")
    else:
        print_error(f"Failed to modify channel: {r.status_code}")

def get_bot_info(*args):
    token = get_token()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print_info(f"Bot: {data.get('username')}#{data.get('discriminator', '0')}")
        print_info(f"ID: {data.get('id')}")
        print_info(f"Verified: {data.get('verified', False)}")
        print_info(f"Created: {data.get('created_at', 'N/A')}")
    else:
        print_error(f"Failed to get bot info: {r.status_code}")

def list_webhooks(*args):
    token = get_token()
    guild_id = get_guild_id()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/webhooks", headers=headers)
    if r.status_code == 200:
        webhooks = r.json()
        for webhook in webhooks:
            print_info(f"{webhook.get('name')} - ID: {webhook.get('id')}")
    else:
        print_error(f"Failed to list webhooks: {r.status_code}")

def server_restore(*args):
    token = get_token()
    guild_id = get_guild_id()
    filename = input("  >> Enter backup filename: ").strip()
    if not filename:
        print_error("No filename entered")
        return
    if not os.path.exists(filename):
        print_error("File not found")
        return
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            backup = json.load(f)
    except Exception as e:
        print_error(f"Error reading file: {e}")
        return
    headers = {"Authorization": f"Bot {token}"}
    print_info("Starting restore...")
    print_info("Creating roles...")
    for role in backup.get('roles', []):
        if role.get('name') == '@everyone':
            continue
        data = {
            'name': role.get('name'),
            'color': role.get('color', 0),
            'hoist': role.get('hoist', False),
            'mentionable': role.get('mentionable', False),
            'permissions': role.get('permissions', '0')
        }
        r, err = discord_api_request(f'guilds/{guild_id}/roles', token, method='POST', json_data=data)
        if err or r.status_code not in [200, 201]:
            print_error(f"Failed to create role {role.get('name')}")
        else:
            print_success(f"Created role: {role.get('name')}")
        time.sleep(0.5)
    print_info("Creating channels...")
    for channel in backup.get('channels', []):
        data = {
            'name': channel.get('name'),
            'type': channel.get('type'),
            'position': channel.get('position', 0),
            'permission_overwrites': channel.get('permission_overwrites', [])
        }
        r, err = discord_api_request(f'guilds/{guild_id}/channels', token, method='POST', json_data=data)
        if err or r.status_code not in [200, 201]:
            print_error(f"Failed to create channel {channel.get('name')}")
        else:
            print_success(f"Created channel: {channel.get('name')}")
        time.sleep(0.5)
    print_success("Restore completed!")

def audit_log(*args):
    token = get_token()
    guild_id = get_guild_id()
    limit = input("  >> Number of entries (default 20): ").strip()
    limit = int(limit) if limit.isdigit() else 20
    if limit > 100:
        limit = 100
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/audit-logs", headers=headers, params={'limit': limit})
    if r.status_code == 200:
        data = r.json()
        entries = data.get('audit_log_entries', [])
        for entry in entries[:limit]:
            print_info(f"Action: {entry.get('action_type', 'Unknown')}")
            print_info(f"  User ID: {entry.get('user_id', 'N/A')}")
            print_info(f"  Target ID: {entry.get('target_id', 'N/A')}")
            print_info(f"  Time: {entry.get('created_at', 'N/A')}")
            if entry.get('reason'):
                print_info(f"  Reason: {entry.get('reason')}")
    else:
        print_error(f"Failed to get audit logs: {r.status_code}")

def bulk_delete(*args):
    token = get_token()
    channel_id = get_channel_id()
    count = input("  >> Number of messages to delete (1-100): ").strip()
    count = int(count) if count.isdigit() else 10
    if count < 1:
        count = 1
    if count > 100:
        count = 100
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, params={'limit': count})
    if r.status_code != 200:
        print_error(f"Failed to fetch messages: {r.status_code}")
        return
    messages = r.json()
    if not messages:
        print_info("No messages found")
        return
    message_ids = [msg['id'] for msg in messages]
    data = {'messages': message_ids}
    r2 = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages/bulk-delete", headers=headers, json=data)
    if r2.status_code == 204:
        print_success(f"Deleted {len(message_ids)} messages")
    else:
        print_error(f"Failed to delete messages: {r2.status_code}")

def permission_checker(*args):
    token = get_token()
    guild_id = get_guild_id()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers=headers)
    if r.status_code != 200:
        print_error(f"Failed to fetch guild: {r.status_code}")
        return
    guild = r.json()
    print_info("1. Check user permissions")
    print_info("2. Check role permissions")
    choice = input("  >> Select option: ").strip()
    if choice == '1':
        user_id = input("  >> Enter user ID: ").strip()
        r2 = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}", headers=headers)
        if r2.status_code == 200:
            member = r2.json()
            permissions = member.get('permissions', '0')
            print_info(f"Permissions: {permissions}")
        else:
            print_error(f"Failed to get member: {r2.status_code}")
    elif choice == '2':
        role_id = input("  >> Enter role ID: ").strip()
        for role in guild.get('roles', []):
            if role['id'] == role_id:
                print_info(f"Permissions: {role.get('permissions', '0')}")
                break
        else:
            print_error("Role not found")
    else:
        print_error("Invalid choice")

def mass_role_assign(*args):
    token = get_token()
    guild_id = get_guild_id()
    role_id = input("  >> Enter role ID: ").strip()
    action = input("  >> Assign or Unassign? (a/u): ").strip().lower()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/members", headers=headers, params={'limit': 1000})
    if r.status_code != 200:
        print_error(f"Failed to fetch members: {r.status_code}")
        return
    members = r.json()
    for member in members:
        user_id = member.get('user', {}).get('id')
        if not user_id:
            continue
        endpoint = f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
        if action == 'a':
            r2 = requests.put(endpoint, headers=headers)
        else:
            r2 = requests.delete(endpoint, headers=headers)
        if r2.status_code in [200, 201, 204]:
            print_success(f"Processed {user_id}")
        else:
            print_error(f"Failed to process {user_id}: {r2.status_code}")
        time.sleep(0.5)

def channel_duplicator(*args):
    token = get_token()
    guild_id = get_guild_id()
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers)
    if r.status_code != 200:
        print_error(f"Failed to fetch channels: {r.status_code}")
        return
    channels = r.json()
    for idx, ch in enumerate(channels, 1):
        ch_type = {0: "Text", 2: "Voice", 4: "Category"}.get(ch.get('type'), "Unknown")
        print_info(f"{idx}. {ch.get('name')} ({ch_type})")
    choice = input("  >> Enter channel number to duplicate: ").strip()
    try:
        idx = int(choice) - 1
        source = channels[idx]
    except:
        print_error("Invalid choice")
        return
    source_id = source.get('id')
    r2 = requests.get(f"https://discord.com/api/v10/channels/{source_id}", headers=headers)
    if r2.status_code != 200:
        print_error(f"Failed to get channel details: {r2.status_code}")
        return
    source_data = r2.json()
    new_name = input("  >> New channel name: ").strip()
    if not new_name:
        new_name = source_data.get('name') + "_copy"
    payload = {
        'name': new_name,
        'type': source_data.get('type'),
        'topic': source_data.get('topic', ''),
        'nsfw': source_data.get('nsfw', False),
        'rate_limit_per_user': source_data.get('rate_limit_per_user', 0),
        'permission_overwrites': source_data.get('permission_overwrites', []),
        'parent_id': source_data.get('parent_id')
    }
    if source_data.get('type') == 2:
        payload['bitrate'] = source_data.get('bitrate', 64000)
        payload['user_limit'] = source_data.get('user_limit', 0)
    r3 = requests.post(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers, json=payload)
    if r3.status_code in [200, 201]:
        print_success(f"Channel duplicated: {new_name}")
    else:
        print_error(f"Failed to duplicate channel: {r3.status_code}")

commands = {
    "webhook_spammer": {"func": webhook_spammer, "description": "Spam a Discord webhook with messages", "usage": "webhook_spammer <url> <message> <count>"},
    "mass_ban": {"func": mass_ban, "description": "Ban multiple users from a server", "usage": "mass_ban"},
    "mass_kick": {"func": mass_kick, "description": "Kick multiple users from a server", "usage": "mass_kick"},
    "server_backup": {"func": server_backup, "description": "Backup server channels, roles, and info to JSON", "usage": "server_backup"},
    "mass_channel_delete": {"func": mass_channel_delete, "description": "Delete all channels in a server", "usage": "mass_channel_delete"},
    "mass_role_delete": {"func": mass_role_delete, "description": "Delete all roles in a server", "usage": "mass_role_delete"},
    "server_info": {"func": server_info, "description": "View detailed server information", "usage": "server_info"},
    "create_invite": {"func": create_invite, "description": "Create a new server invite", "usage": "create_invite"},
    "prune_members": {"func": prune_members, "description": "Prune inactive members from a server", "usage": "prune_members"},
    "list_channels": {"func": list_channels, "description": "List all channels in a server", "usage": "list_channels"},
    "list_roles": {"func": list_roles, "description": "List all roles in a server", "usage": "list_roles"},
    "delete_all_webhooks": {"func": delete_all_webhooks, "description": "Delete all webhooks in a server", "usage": "delete_all_webhooks"},
    "get_user_info": {"func": get_user_info, "description": "Get detailed user information", "usage": "get_user_info"},
    "get_member_info": {"func": get_member_info, "description": "Get member information from a server", "usage": "get_member_info"},
    "list_emojis": {"func": list_emojis, "description": "List all emojis in a server", "usage": "list_emojis"},
    "delete_emoji": {"func": delete_emoji, "description": "Delete an emoji from a server", "usage": "delete_emoji"},
    "create_channel": {"func": create_channel, "description": "Create a new channel in a server", "usage": "create_channel"},
    "create_role": {"func": create_role, "description": "Create a new role in a server", "usage": "create_role"},
    "modify_channel": {"func": modify_channel, "description": "Modify an existing channel", "usage": "modify_channel"},
    "get_bot_info": {"func": get_bot_info, "description": "Get information about the bot", "usage": "get_bot_info"},
    "list_webhooks": {"func": list_webhooks, "description": "List all webhooks in a server", "usage": "list_webhooks"},
    "server_restore": {"func": server_restore, "description": "Restore server from backup file", "usage": "server_restore"},
    "audit_log": {"func": audit_log, "description": "View server audit log entries", "usage": "audit_log"},
    "bulk_delete": {"func": bulk_delete, "description": "Bulk delete messages from a channel", "usage": "bulk_delete"},
    "permission_checker": {"func": permission_checker, "description": "Check user or role permissions", "usage": "permission_checker"},
    "mass_role_assign": {"func": mass_role_assign, "description": "Mass assign or unassign a role", "usage": "mass_role_assign"},
    "channel_duplicator": {"func": channel_duplicator, "description": "Duplicate an existing channel", "usage": "channel_duplicator"}
}