---
title: '[[《Learn PowerShell in a month of Lunches》]]'
date: '2025-09-16'
tags: []
---
Shell：本质上是一段程序，负责接收用户输入的命令，解析后交给操作系统执行，然后把结果再输出给你。

Terminal：终端负责提供一个**用户界面**来运行 Shell，处理输入输出（键盘输入、屏幕显示）。

### 帮助系统
1. `Help` 空格翻页，q 离开，Enter 下一行。
2. `Get-Help` 类似于 help。
3. `Get-Command ` 会显示 cmdlet，cmdlet 全部都是 Verb-Noun 命名的，寻找的时候，可以用 `-verb`、`-noun` 参数来找对应的命名。
4. syntax 之中名字和值一起在 `[]` 里面是可选择的参数，有默认值。
5. 位置参数，如果一个参数的名字用 `[]` 扩起来，那么这个参数就无需写参数名，可以直接写参数值。
6. 如果参数是 `<String[]>` 表示可以输入一个字符串，或者多组字符串，字符串之间用逗号隔开，每个字符串可用单引号扩起来。整个字符串组不要用单引号扩起来。
7. `[<SwitchParameter>]` 参数代表没有参数值需要输入，这些参数的参数名不可缺省。

### 指令
1. cmdlet：PowerShell 的核心命令单元，用.Net Core Language 编写。
2. function，类似 cmdlet， 用 PowerShell 的脚本语言编写。
3. powershell 可以兼容很多种类的指令，但是有些特殊符号很可能也会被读取（比如`$`）。这种情况下要告诉它不要这样读取
4. `New-Alias` 创建新的别名 `Get-Alias` 去的所有的别名。

### 文件系统
1. `New-Item name -ItemType Directory(file)` 
2. `-LiteralPath` 将所有字符都当作 path，不看 `*`、`?` 这些 wildcard。
3. **HKEY_CURRENT_USER（HKCU）** 是 Windows 注册表里**当前登录用户的专属配置区**。位置是  `HKCU:\`
4. **PSProvider** 是把各种“数据存储”适配成像磁盘一样可浏览的接口的“适配层”。有了它，你就能用同一套命令（Get-ChildItem, Set-Item, Get-ItemProperty…）去操作**文件系统、注册表、证书、环境变量、函数、别名**等，看起来都像在某个“盘符”里走路径。
5. `Dir` 在 PowerShell 之中等同于 `Get-ChildItem` 。
	1. **-Filter**：由底层 **Provider**（比如 NTFS 文件系统、Registry 提供程序）直接处理。受 Provider 限制，文件系统支持通配符（*.csv、*.log）。
	2. **-Include**：先列出一堆结果，再由 PowerShell 在结果集里“挑出来”。需要多模式时（如同时要 `*.csv` 和 `*.txt`）
	3. **-Exclude**：同样需要路径带 * 或配合 -Recurse。
	4. **-Recurse**：加上这个参数之后会把所有子目录都列出来。可以用 `-Depth num` 限制深度。

### 管道系统
1. `|` 表示取得输出并且进行下一步动作。
2. `Export-CSV csvname` 输出为 csv。
3. `| select-Object Threads` 选择线程
4. `| ConvertTo-Json(CSV)` 改成某种文件，包括 xml / csv / Html / yaml 等。有嵌套的时候尽量生成 json，
5. climxl 格式能够保证输出之后再 `Import-Clixml` 在里面的格式相同。但是只能被当前 user 解码。
6. `compare-object`：两个参数 `-ReferenceObject` 和 `-DifferenceObject` ，里面的 SideIndicator ` => ` 表示只在右边出现，` <= ` 表示只在左边出现。对于对比 text file 并不擅长。
7. `ConvertTo-格式 | Out-File filename` 等同于 `Export-格式`。`NoClobber` 可以防止覆盖已经有的文件。注意如果传出 csv 用 excel 读取并且包含中文的话，格式要加上 `-Encoding utf8BOM`
8. `Stop Process` 停止某个过程，可以通过 `-WhatIf`  来看看后果
9. `Import-格式` 相比于 `Get-Content` 会进行更精细地读取并且排版。

### module 插件
1. `Import-Module` 加载插件，用 `Get-Content Env:/PSModulePath` 来查看插件应该放在哪个位置。只要插件放在了对应的位置就可以 `Get-Help` ，之后就可以直接 run 了，PowerShell 会帮你加载。
2. `Compress-Archive` 压缩文件，有 `-Path` `-Destination-Path` 两个参数表示位置。


### object
1. Powershell 不像 bash 等对于文字进行处理，处理的是一个一个的 object。用 `gm` 来获得 object 的属性和方法等 member。附属于一个 object 的称为 member。`gm` 得到的结果也会失去原有的很多 member。
2. `Sort-Object` 将对象进行排序，可以用 `-Desc` 进行倒序排列。
3. `Select-Object` 选择只展示某些你指定的 property，并不是选择某些 object 的意思，而是选择展示的 property。
	1. Powershell 实现时会新建一个“自定义对象”（PSCustomObject）此时已经失去了很多的 member。
	2. `-ExpandProperty` 把对象里的某个属性“展开”为该属性的值原始对象（而非正常 Property 中的 object）。

### 管道
1. pipeline 读取的方式有两种，一种是发现读取的类型匹配后面参数的类型，那么就能读取（ByValue）。另外一种是管道的对象中具有属性，这个属性名称与参数的属性名称匹配，那么可以用属性值作为参数值（ByProperty）。
2. `import-csv` 之后可以使用 `@{name/label/n = '属性名';expression/e = {$_.CSV列名}}` 来重命名并显示某个属性名为另外一个名字。
3. 可以使用 `()` 扩起来某个指令，然后让它作为另外一个指令的参数。
4. 查看某个输出的类型 `().GetType().Name`

### 格式化
1. 首先看一下是否有 predefined view。然后看一下是否有任何人已经声明了这种对象的展示属性。若有5个或以上属性，它展示一个 table，否则展示一个 list。
2. `Format-Table` 横向展开:
	1. `-Property` 需要展示哪些属性。
		1. `@{name = 'Colname';expression={$_.expName -as[type]}; foramt-string = 'F2';align = 'right'} -AutoSize` 其中 `$_` 表示当前变量。后面的 type 可以用 int 等。还可以在 expName 后对结果进行操作，比如说加减乘除，并且对于大小，能识别 KB、MB、GB、TB、PB。
	2. `GroupBy` 需要在 `Sort-Object` 之后使用，结果进行分类展示。
	3. `Wrap` 会将所有的信息都显示出来，而不会截断。
3. `Format-List` 纵向展开每个属性。
4. `Format-Wide`  只显示一种属性的值。一般是两列，可以用 `-col` 调整为 4 列。
5. 正常的输出之后跟着 `Out-Host` 表示输出到当前界面。
6. 使用 `Microsoft.PowerShell.GraphicalTools` 可以将其输出到 Gridview 之中。`Out-GridView`，不接受任何 format 的 cmdlet。
7. 注意：
	1. 唯一能接收 format 得到的结果的是 `out-file` 和 `out-host` 其他都会产生意想不到的结果。
	2. 一次处理一种属性的对象。

### 过滤
1. 比较方式：`-eq`、`-ne`、`-ge`、`-le`、`-gt`、`lt`。最后四个的差别是大于等于和大于。`-and`、`-or`、`-not(!)` 也支持。
2. 在前面加上 `c` 表示区分大小写。前面加上 `i` 表示忽略大小写。
3. 定义了 `$False` 和 `$True` 代表布尔值。
4. wildcard：`*` 、`?`、`[]` 分别表示零个或多个，一个以及范围字符。可以用 `-like` 或者 `-notlike` 来比较。`-match` 正则表达式匹配。
5. 在 `Where-Object -FileterScript` 之中使用，其中 `-FilterScript` 可省略。


### 远程连接
1. powershell 使用后台服务中 Windows remote Management 中的 WSMan。MacOS 和 Linus 使用的是 standard secure shell（SSH）。
2. 输出从 object 变为 XML 进行传输，然后从 XML 变回 Object。

|**参数**|**属于哪类**|**用途**|**底层协议**|**平台**|
|---|---|---|---|---|
|-ComputerName|核心 remoting|连接远端 Windows，WinRM/WSMan|5985/5986|Windows-only|
|-HostName|核心 remoting|连接任何启用 SSH 的机器|SSH (22)|跨平台|
|-Server|各模块自带|特定服务端地址（SQL, Exchange, AzureAD…）|视模块实现|模块特定|

### 后台工作和多任务
1. 程序工作 `Start-Job -scriptblock {script} -WorkingDirectory path` 适用于长期工作。
2. 线程工作 `Start-ThreadJob -scriptblock {script}` 适用于短期工作，最多 10 个线程。
3. 远程工作 `invoke-command -command {script} -hostname host -asjob -jobname JobName`
4. 查看现在的工作 `Get-Job`。里面的 HasMoreData 一栏之中表示是否还有结果没有 print 出来。
5. 取得工作的结果 `receive-job` 。不加入参数的话会显示这个工作以及其所有子工作的结果。将会清空工作中的缓存，下次调用这个命令不会得到任何结果，除非加上 `keep` 参数。工作错误输出也会在其中。z
6. `Remove-Job` 将一个 job 删除，并且将任何缓存清除。
7. `Stop-Job` 停止一项正在进行的工作，能获得当前的输出。
8. `Wait-Job` 停止 powershell 的一切行动直到某个 job 完成。
9. job 的生命周期是 powershell 存续期间，关闭之后所有的都会关闭。


### 成批处理任务
1. 成批处理的任务通常带有 `-PassThru` 变量，可以打印出每一个结果。
2. 可以使用 `For-each-Object -Process{Script}` 对于那些没有批量处理 cmdlet 的对象，对每个对象分别进行处理。使用 `-Parallel{Script}` 参数可以让各个 Object 并行进行。正常情况下只能 5 个同时进行，在前面加上 `-ThrottleLimit 10` 能让 10 个同时进行。

### 变量
1. 变量声明 `$VarName = ` name 可以是数字、下划线、字母，如果要有空格，就要用大括号括起来。变量的生存周期就是 Powershell 的生存周期。变量视为储存类型的 object。
2. 如果是双引号，那么字符串变量会自动识别 `$` 符号，并用对应的变量进行替换，但是这只会发生在初始创建这个字符串的时候。
3. 使用 `ToUpper` 、`ToLower` 等 method 会创建一个全新的字符串，不会修改原来的字符串。
4. 斜点符号等同于特殊符号，可以让 Powershell 忽略 `$`，也可以打出换行符等符号。
5. 储存多个 object：
	1. 可以使用 `,` 分开各个 object，取得一个 list。之后可以使用 index 来获取各个 object，并且支持负数获取倒数几个 object。
	2. 如果要修改某个变量，必须使用该变量 = 某个表达式。
	3. 可以用 pipeline，然后使用 `ForEach-Object` 对每个储存的 object 进行相同的操作。
6. 将 cmdlet 储存在变量之中，使用 `$val.property` 去取得 property 的时候，可以取得 cmdlet 结果中的 property，等同于 `cmdlet | Select-Object -ExpandProperty property` 注意这里直接还原了对象，而非正常的输出 object。
7. 双引号如果要在其中加入 cmdlet 语句，那么需要 `$(script)`。包括 `$var[0]` `$var.name` 这样的都需要放在括号之中，否则只会识别出前面的 var 后面的直接当作文字。
8. 在使用变量的时候，可以用 `[type]$var` 将其转换成某种 type。可以有 single、double、int、string、char、xml 等格式。
9. cmdlet 包括 `Get-Variable` `New-Variable` `Remove-Variable` `Clear-Variable` `Set-Variable`。


### 输入和输出交互
1. `Read-Host "Prompt"` 显示一个提示语，然后从用户获取输入的文字。
2. `write-Host "words"` 直接将输入在电脑上输出（无法经过 pipeline），并且可以通过 `-Foreground` 和 `-BackgroundColor` 来调节颜色。
3. `Write-Output "words"` 先将信息写入 pipeline 然后 `out-host`，中间可以插入其他行为。
4. `Write-Progress` 可以显示当前进度条
5. `Write-Verbose` 主要用于写脚本/模块的调试或详细执行信息。

### 脚本
1. 用 back tick 在一行的末尾，可以将下一行接在这一行的代码后。
2. 想要脚本有参数，那么可以 `param($var1 = 默认值1, $var2 = 默认值2)`
3. Script 之中任何在 `#` 后面的都会视为注释，多行注释使用 `<##>`。
4. 作用域：function、script、global。
5. `[CmdLetBinding()]` 在 param 前面加
	1. 可以将参数设为必须，在参数前加上 `[Parameter(Mandatory = $True)]` 
	2. 可以设置参数的别名，在参数前面加上 `[Alias('别名')]`
	3. 设置参数的有效值：`[ValidateSet(val1, val2)]


### 正则表达式
1. `\w` 字符，表示字母数字、下划线，但不包括标点符号和空格。`\W` 表示 space 字符和标点符号。
2. `\d` 从0-9的数字，`\D` 表示任何非数字。
3. `\s` 任何 whitespace 字符，包括 tab，spcae 和 return，`\S` 表示任何非 whitespace 字符。
4. `.` 任何字符。
5. `[abcde]` 任何在中括号之中包含的单个字符。`[a-z]` 任何在这个范围内的一个或者多个字符。`[^abcdde]` 任何不在这个集合内的一个或者多个字符。
6. `?` 0 个或一个字符。`*` 0或多个前一个字符，比如 `ca*r` 可以匹配 `cr` 。`+` 一个或者多个前一个字符。`(ca)r` 匹配 `cacar` 。
7. `\` 转义字符。
8. 前面的匹配都表示只要有这样的模式就可以。`^` 代表从字符串开头进行匹配。 `^car` 表示必须开头是 car。
9. `a{1, 3}` 表示至少有 1 个a，最多有三个 a。`a{1}` 表示恰好有一个 a。
10. `$` 表示字符串结尾。
11. `-match` 前面表示需要匹配的字符串，后面是正则表达式。
12. `Select-String pattern` 如果传入的是 FileInfo 对象，那么就会直接在文件之中着匹配的字符串（而非寻找文件名）。

### 循环
1.  `foreach($temp IN $array){Do}` 循环。可以使用 `a..b` 用于创建包含 a 和 b 的从 a 到 b 的数组。
2. `foreach-Object` 主要用在 pipeline 之中，用于对每个 pipeline 产生的 object 进行循环。这里是从 `item[0]` 开始的。可以使用 `-Parallel` 让他们并行进行。
3. `While (con) {Do}` 这里如果定义了 `$n` 支持 `$n++` 操作。

### 错误处理
1. `$Error` 变量，当前 session 之中的错误，即 `ErrorAction` 之中的错误。
2. `ErrorVariable` 可以在语句后面写上 `-ErrorVariable a` 来写入错误进入变量 a，只会保存一条错误，除非使用 `+a`
3. 使用 `-ErrorAction` 对错误进行处理，默认方式为 `$ErrorActionPreference`
	1. `break` 进入 debugger
	2. `continue` 展示错误信息并继续
	3. `Ignore` 不展示错误信息并继续。不能设置为常量，只能设置为一次性。
	4. `Inquire` 展示错误信息，并询问你接下来怎么做。
	5. `SilentlyContinue` 不展示错误信息并继续。
	6. `Stop` 展示错误信息并且停止，创建一个 `ActionPreferenceStopException` object 进入 error stream
	7. `Suspend` 暂停这个 workflow，可以进行手动恢复，也不能设置为常量。
4. `Try catch finally（无论是否 catch 都会运行）` 捕获所有的会停止的错误，如果想要非停止错误也要捕获，那么要将 `ErrorAction` 设置为 `stop`

### debug
1. `$DebugPreference = 'continue'`  打印调试信息。

### tips and tricks
1. 几个变量：`$pshome` powershell 的安装位置。`$home` 用户文件夹
2. 查看所有的有关设置的 profile：`$Profile | Format-List -force`
3. Prompt 是终端里等待你输入命令时显示的提示符，本质是一个可修改的 prompt 函数。
	1. `$host.UI.RawUI.WindowTitle = "$env:username"` 可以更改 title bar
	2. 可以设置里面的各种字体，error、warning、debug 的字体颜色。
4. 操作符：
	1. `-as` 进行类型转换 `[int]` `[string]` `[xml]` `[single]` 等。`-is` 返回 True 或者 false 判断是否是该类型。
	2. `string -replace "sourse", "tar"` 用 tar 替换 string 中的所有 source。
	3. `-join '|'` `-split '|'` 分别将 array 用 `|` 连接起来成为字符串或者字符串拆成 array
	4. `-like` 用于 wildcard 匹配
	5. `a -contain b` 用于在一个组合之中查看某个元素b是否在集合a里面。`b -in a` 代表相同的意思
5. 设置默认变量值。`$PSDefaultParameterValues.Add('<CmdletName>:<ParameterName>', <value>)` 
	- `*` 表示匹配所有命令。
	- `<CmdletName>` 可以是具体命令，如 Invoke-Command。
	- `<ParameterName>` 就是参数名，比如 Credential。
	- `<value>` 可以是实际值，也可以是一个**脚本块** {}。
6. 脚本块：
	1. 可以用 `$var = {scriptblock}` 之后用 `&$var` 来获取脚本块的输出。
	2. 哈希表使用 `@{}` 

其他资源：
1. 数据库组件：https://dbatools.io。
2. https://powershell.org
3. https://youtube.com/powershellorg
4. https://jdhitsolutions.com
5. https://devopscollective.org
