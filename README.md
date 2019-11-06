# Dao Ke Dao (道可道) -- Message Module (Python)

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/dimchat/dkd-py/blob/master/LICENSE)
[![Version](https://img.shields.io/badge/alpha-0.6.4-red.svg)](https://github.com/dimchat/dkd-py/wiki)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/dimchat/dkd-py/pulls)
[![Platform](https://img.shields.io/badge/Platform-Python%203-brightgreen.svg)](https://github.com/dimchat/dkd-py/wiki)

This [document](https://github.com/dimchat/DIMP/blob/master/DaoKeDao-Message.md) introduces a common **Message Module** for decentralized instant messaging.

Copyright &copy; 2018-2019 Albert Moky

- [Envelope](#envelope)
    - Sender
    - Receiver
    - Time
- [Content](#content)
    - [Type](#content-type)
    - Serial Number
- [Message](#message)
    - [Instant Message](#instant-message)
    - [Secure Message](#secure-message)
    - [Reliable Message](#reliable-message)

## <span id="envelope">0. Envelope </span>

### Message Envelope

```javascript
/* example */
{
    "sender"   : "moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk",
    "receiver" : "hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj",
    "time"     : 1545405083
}
```

## <span id="content">1. Content</span>

```javascript
/* example */
{
    "type"     : 0x01,      // message type
    "sn"       : 412968873, // serial number (message ID in conversation)
    
    "text"     : "Hey guy!"
}
```

### <span id="content-type">Message Content Type</span>

```javascript
enum {
    DIMContentType_Unknown = 0x00,
    
    DIMContentType_Text    = 0x01,
    
    DIMContentType_File    = 0x10,
    DIMContentType_Image   = 0x12, // photo
    DIMContentType_Audio   = 0x14, // voice
    DIMContentType_Video   = 0x16,
    
    DIMContentType_Page    = 0x20, // web page
    
    // quote an exists message and reply it with text
    DIMContentType_Quote   = 0x37,
    
    // system command
    DIMContentType_Command = 0x88,
    
    // top-secret message forward by proxy (Service Provider)
    DIMContentType_Forward = 0xFF
};
```

## <span id="message">2. Message</span>

When the user want to send out a message, the client needs TWO steps before sending it:

1. Encrypt the **Instant Message** to **Secure Message**;
2. Sign the **Secure Message** to **Reliable Message**.

Accordingly, when the client received a message, it needs TWO steps to extract the content:

1. Verify the **Reliable Message** to **Secure Message**;
2. Decrypt the **Secure Message** to **Instant Message**.

```javascript
    Message Transforming
    ~~~~~~~~~~~~~~~~~~~~

    Instant Message  <-->  Secure Message  <-->  Reliable Message
    +-------------+        +------------+        +--------------+
    |  sender     |        |  sender    |        |  sender      |
    |  receiver   |        |  receiver  |        |  receiver    |
    |  time       |        |  time      |        |  time        |
    |             |        |            |        |              |
    |  content    |        |  data      |        |  data        |
    +-------------+        |  key/keys  |        |  key/keys    |
                           +------------+        |  signature   |
                                                 +--------------+
    Algorithm:
        data      = password.encrypt(content)
        key       = receiver.public_key.encrypt(password)
        signature = sender.private_key.sign(data)

```

### <span id="instant-message">Instant Message</span>

```javascript
/* example */
{
    //-------- head (envelope) --------
    "sender"   : "moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk",
    "receiver" : "hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj",
    "time"     : 1545405083,
    
    //-------- body (content) ---------
    "content"  : {
        "type" : 0x01,      // message type
        "sn"   : 412968873, // serial number (ID)
        "text" : "Hey guy!"
    }
}
```

content -> JsON string: ```{"sn":412968873,"text":"Hey guy!","type":1}```

### <span id="secure-message">Secure Message</span>

```javascript
/**
 *  Algorithm:
 *      string = json(content);
 *      PW     = random();
 *      data   = encrpyt(string, PW);      // Symmetric
 *      key    = encrypt(PW, receiver.PK); // Asymmetric
 */
{
    //-------- head (envelope) --------
    "sender"   : "moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk",
    "receiver" : "hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj",
    "time"     : 1545405083,
    
    //-------- body (content) ---------
    "data"     : "9cjCKG99ULCCxbL2mkc/MgF1saeRqJaCc+S12+HCqmsuF7TWK61EwTQWZSKskUeF",
    "key"      : "WH/wAcu+HfpaLq+vRblNnYufkyjTm4FgYyzW3wBDeRtXs1TeDmRxKVu7nQI/sdIALGLXrY+O5mlRfhU8f8TuIBilZUlX/eIUpL4uSDYKVLaRG9pOcrCHKevjUpId9x/8KBEiMIL5LB0Vo7sKrvrqosCnIgNfHbXMKvMzwcqZEU8="
}
```

### <span id="reliable-message">Reliable Message</span>

```javascript
/**
 *  Algorithm:
 *      signature = sign(data, sender.SK);
 */
{
    //-------- head (envelope) --------
    "sender"   : "moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk",
    "receiver" : "hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj",
    "time"     : 1545405083,
    
    //-------- body (content) ---------
    "data"      : "9cjCKG99ULCCxbL2mkc/MgF1saeRqJaCc+S12+HCqmsuF7TWK61EwTQWZSKskUeF",
    "key"       : "WH/wAcu+HfpaLq+vRblNnYufkyjTm4FgYyzW3wBDeRtXs1TeDmRxKVu7nQI/sdIALGLXrY+O5mlRfhU8f8TuIBilZUlX/eIUpL4uSDYKVLaRG9pOcrCHKevjUpId9x/8KBEiMIL5LB0Vo7sKrvrqosCnIgNfHbXMKvMzwcqZEU8=",
    "signature" : "Yo+hchWsQlWHtc8iMGS7jpn/i9pOLNq0E3dTNsx80QdBboTLeKoJYAg/lI+kZL+g7oWJYpD4qKemOwzI+9pxdMuZmPycG+0/VM3HVSMcguEOqOH9SElp/fYVnm4aSjAJk2vBpARzMT0aRNp/jTFLawmMDuIlgWhBfXvH7bT7rDI="
}
```

(All data encode with **BASE64** algorithm as default)
