open(url)：target=绝对https://xxx.com、相对/xxx.html(base url+/xxx.html)

pause：target=x ms

goback:no target,no value

refresh:no target,no value

click:target= id=xx

type(输入)：target= id=xx,value=xx

close:no target,no value



id、name、class值

tag_name标签种类 find_element**s**

link_text、partial_link_text a超链接

Xpath元素路径：文本[text()='']、属性/多属性[@属性 and @属性]、包含[contains(@属性,'')]、层级'/'-'//'

Css选择器：id#、class.、标签、[属性=''] [属性='']、包含[属性*='']、层级'>'-' '



操作：click\clear\send_keys

信息：size\text\get_attribute('属性')\is_displayed()\is_enabled()\is_selected()







playwright

一组元素

```python
locators = page.locator('div').all()
```









写一个浏览器插件来实现对浏览器中全局匹配字段的高亮效果是可行的。下面是一个简单的示例，展示如何使用 JavaScript 和浏览器扩展（Chrome 插件）来实现这个功能：

1. 首先，创建一个文件夹，作为插件的根目录。
2. 在根目录下创建一个 `manifest.json` 文件，并添加以下内容：

json

复制

```
{
  "manifest_version": 2,
  "name": "字段高亮插件",
  "version": "1.0",
  "description": "根据导入的字典对浏览器中全局匹配的字段进行高亮。",
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"]
    }
  ],
  "permissions": ["tabs", "activeTab"],
  "browser_action": {
    "default_popup": "popup.html",
    "default_title": "字段高亮插件"
  },
  "icons": {
    "16": "icon.png",
    "48": "icon.png",
    "128": "icon.png"
  }
}
```

这是扩展的清单文件，其中指定了扩展的名称、版本、描述以及一些必要的权限。还定义了内容脚本 `content.js` 和弹出窗口 `popup.html`。

1. 在根目录下创建一个 `content.js` 文件，并添加以下内容：

javascript

复制

```
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'highlight') {
    const dictionary = request.dictionary;
    const elements = document.getElementsByTagName('*');

    for (let i = 0; i < elements.length; i++) {
      const element = elements[i];

      for (let j = 0; j < dictionary.length; j++) {
        const keyword = dictionary[j];

        if (element.innerHTML.includes(keyword)) {
          const regex = new RegExp(`(${keyword})`, 'gi');
          const highlightedText = element.innerHTML.replace(regex, '<span style="background-color: yellow;">$1</span>');
          element.innerHTML = highlightedText;
        }
      }
    }
  }
});
```

这是内容脚本，它监听来自插件的消息，并根据接收到的字典对页面中的元素进行高亮处理。通过遍历页面上的所有元素，对每个元素的内容进行匹配，如果匹配成功，则将匹配的部分用 `<span>` 标签包裹并添加黄色背景色。

1. 在根目录下创建一个 `popup.html` 文件，并添加以下内容：

html

复制

```
<!DOCTYPE html>
<html>
<head>
  <title>字段高亮插件</title>
  <script src="popup.js"></script>
</head>
<body>
  <h1>字段高亮插件</h1>
  <textarea id="dictionary-input" rows="10" cols="30" placeholder="请输入要匹配的关键字，每行一个"></textarea>
  <button id="highlight-button">高亮</button>
</body>
</html>
```

这是弹出窗口的 HTML 文件，其中包含一个文本输入框和一个按钮。用户可以在文本输入框中输入要匹配的关键字，并点击按钮来触发高亮操作。

1. 在根目录下创建一个 `popup.js` 文件，并添加以下内容：

javascript

复制

```
document.addEventListener('DOMContentLoaded', function() {
  const highlightButton = document.getElementById('highlight-button');
  const dictionaryInput = document.getElementById('dictionary-input');

  highlightButton.addEventListener('click', function() {
    const dictionary = dictionaryInput.value.split('\n').filter(Boolean);

    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      const message = {
        action: 'highlight',
        dictionary: dictionary
      };

      chrome.tabs.sendMessage(tabs[0].id, message);
    });
  });
});
```

这是弹出窗口的 JavaScript 文件，它监听高亮按钮的点击事件，并将输入的关键字作为消息发送给内容脚本 `content.js`。

1. 将一个适当大小的 `icon.png` 图像文件放在根目录下，作为插件的图标。
2. 打开谷歌浏览器，转到扩展程序页面（chrome://extensions/）。
3. 在扩展程序页面的右上角启用开发者模式。
4. 点击“加载已解压的扩展程序”按钮，选择插件的根目录。
5. 完成以上步骤后，插件就会加载并显示在扩展程序栏中。
6. 点击插件图标，弹出弹出窗口。
7. 在文本输入框中输入要匹配的关键字，每行一个。
8. 点击“高亮”按钮，插件将会在当前浏览器页面中根据输入的关键字进行高亮。

请注意，这只是一个简单的示例，仅用于演示如何实现基本的字段高亮功能。你可以根据自己的需求进行扩展和改进。另外，这个示例是基于 Chrome 插件的开发，如果你希望在其他浏览器上运行，可能需要进行相应的调整。





插件的目录结构可以按照以下方式组织：

复制

```
highlight-plugin/
  ├── manifest.json
  ├── content.js
  ├── popup.html
  ├── popup.js
  └── icon.png
```

上述目录结构是一种常见的组织方式，但你也可以根据自己的喜好进行调整。

- `manifest.json` 是插件的清单文件，其中定义了插件的基本信息、内容脚本和弹出窗口的路径等。
- `content.js` 是内容脚本，它负责在页面中执行脚本，并根据接收到的消息对页面元素进行高亮处理。
- `popup.html` 是弹出窗口的 HTML 文件，用于用户输入要匹配的关键字。
- `popup.js` 是弹出窗口的 JavaScript 文件，它监听用户的操作，并将输入的关键字传递给内容脚本。
- `icon.png` 是插件的图标文件，用于在浏览器的扩展栏中显示插件图标。

这种目录结构是一种基本的示例，你可以根据自己的需求进行调整和扩展。





当开发浏览器插件时，还有一些其他的概念和技术可以帮助你实现所需的功能。以下是一些可能对你有帮助的信息：

1. 内容脚本：内容脚本是插件中与浏览器页面交互的主要脚本。它可以访问页面的 DOM 结构，并与页面进行通信。在上面的示例中，我们使用内容脚本 `content.js` 来遍历页面元素，并应用高亮效果。
2. 插件清单文件（manifest.json）：插件清单文件是插件的配置文件，用于指定插件的名称、版本、描述、文件路径等信息。它还定义了插件的权限和行为，如何与浏览器进行交互。在示例中，我们使用了 `manifest.json` 文件来配置插件的基本信息和内容脚本的位置。
3. 消息传递：插件中不同的脚本之间可以通过消息传递进行通信。在示例中，我们使用 `chrome.runtime.onMessage` 监听来自插件的消息，并在内容脚本中处理接收到的消息。通过消息传递，你可以从弹出窗口发送消息到内容脚本，以触发相应的操作。
4. 弹出窗口：弹出窗口是插件中的一个交互界面，可以用于接收用户的输入或显示插件的状态。在示例中，我们使用了一个简单的弹出窗口 `popup.html`，其中包含一个文本输入框和一个按钮。用户可以在文本输入框中输入要匹配的关键字，并点击按钮来触发高亮操作。
5. 权限：浏览器插件需要明确申明所需的权限，以便访问特定的功能或信息。在示例中，我们在 `manifest.json` 文件中添加了 `"permissions": ["tabs", "activeTab"]`，以获取对浏览器标签页和当前活动标签页的访问权限。
6. 跨浏览器兼容性：需要注意的是，不同的浏览器可能有不同的插件开发机制和 API。示例中的代码是基于 Chrome 插件开发的，如果你希望在其他浏览器上运行，可能需要进行相应的调整或使用其他的插件开发技术。
7. 调试和测试：在开发插件时，可以使用浏览器的开发者工具来调试和测试插件的代码。你可以通过控制台输出日志、设置断点等方式进行调试，以确保插件的正常运行和预期效果。

以上是一些关于开发浏览器插件的基本概念和技术。如果你希望深入学习插件开发，建议查阅相关浏览器的插件开发文档，如 Chrome 扩展开发文档、Firefox 插件开发文档等。这些文档提供了更详细的指导和示例，帮助你更好地理解和应用插件开发技术。







要在浏览器中实现对匹配值的高亮效果，你可以使用浏览器插件来完成。下面是一个示例插件的基本结构和实现思路：

1. 创建插件目录结构：按照之前提到的插件目录结构创建一个新的插件项目。
2. 编写清单文件（`manifest.json`）：在清单文件中指定插件的基本信息、权限和脚本等。例如：

json

复制

```
{
  "manifest_version": 2,
  "name": "Highlight Idioms",
  "version": "1.0",
  "description": "A browser extension to highlight idioms in the specified local file",
  "permissions": ["file:///*"],
  "content_scripts": [
    {
      "matches": ["http://*/*", "https://*/*"],
      "js": ["content.js"],
      "run_at": "document_idle"
    }
  ],
  "icons": {
    "16": "icon16.png",
    "48": "icon48.png",
    "128": "icon128.png"
  }
}
```

在上述示例中，我们指定了插件的名称、版本、描述以及需要的权限。`"permissions"` 字段用于声明插件需要访问的文件 URL 权限。`"content_scripts"` 字段用于指定在哪些网页上注入内容脚本，并在页面加载完成后运行。

1. 编写内容脚本（`content.js`）：内容脚本负责在页面中查找并高亮匹配的成语。以下是一个简单的示例：

javascript

复制

```
// 从本地文件中获取成语列表
fetch('path/to/idiom/file.txt')
  .then(response => response.text())
  .then(text => {
    const idioms = text.split('\n');

    // 遍历页面中的文本节点，匹配并高亮成语
    const textNodes = document.evaluate('//text()', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
    for (let i = 0; i < textNodes.snapshotLength; i++) {
      const node = textNodes.snapshotItem(i);
      const content = node.textContent;

      // 遍历成语列表，匹配并高亮
      idioms.forEach(idiom => {
        const regex = new RegExp(`\\b${idiom}\\b`, 'gi');
        const replacedContent = content.replace(regex, `<span style="background-color: yellow;">$&</span>`);
        if (replacedContent !== content) {
          const wrapper = document.createElement('div');
          wrapper.innerHTML = replacedContent;
          node.parentNode.replaceChild(wrapper, node);
        }
      });
    }
  });
```

在上述示例中，我们使用 `fetch` 函数从指定的本地文件中获取成语列表，并遍历页面中的文本节点来匹配和高亮成语。使用正则表达式进行匹配，并将匹配的部分用 `<span>` 标签包裹，并添加黄色背景色。

1. 添加图标和其他资源：将插件所需的图标等资源文件放置在适当的位置，并在清单文件中进行引用。
2. 打包和加载插件：根据不同浏览器的要求，将插件文件打包为相应的格式（如 Chrome 的 CRX 文件或 Firefox 的 XPI 文件），然后在浏览器中加载插件。

请注意，上述示例是一个简化的实现，可能需要根据实际需求进行修改和扩展。同时，本地文件的访问可能受到浏览器的安全策略限制，你可能需要进行额外的配置或授权。