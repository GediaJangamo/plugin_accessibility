# plugin_accessibility

Este projeto faz parte do Trabalho de Conclusão de Curso (TCC) da estudante Gédia Jangamo,
no curso de Engenharia de Tecnologias e Sistemas de Informação. Universidade Joaquim Chissano

Tema: Implementação de Tecnologias Assistivas no Sistema Integrado de Gestão Académica (SIGA):
Promovendo a Inclusão Digital de Estudantes com Deficiência Visual Caso de Estudo:
Universidade Eduardo Mondlane – Faculdade de Letras e Ciências Sociais, Faculdade de Educação e Faculdade de Filosofia.


# 🎧 Plugin de Acessibilidade para Sistemas Académicos com IA

Este projeto é um **plugin de acessibilidade inteligente** desenvolvido em **Python e Django**, com foco na **inclusão digital de estudantes com deficiência visual**. O plugin pode ser incorporado a sistemas robustos já existentes, como o **SIGA (Sistema Integrado de Gestão Académica)**, para tornar suas funcionalidades mais acessíveis por meio de **comandos de voz, leitura de conteúdo e navegação inteligente** — tudo isso funcionando mesmo em ambientes com **internet fraca ou indisponivel**.

## 🧩 O que este plugin faz?

📢 **Navegação por Voz**: permite que estudantes usem comandos de voz para navegar no sistema (ex: "ver notas", "fazer matrícula").
🧠 **Leitura de Conteúdo**: usa síntese de voz para ler textos da tela para estudantes com cegueira total ou baixa visão.
🌐 **IA Adaptativa**: deteta automaticamente a qualidade da conexão e escolhe entre:
IA local (offline)
IA online (por exemplo, integração futura com API da HandTalk ou outros recursos)
🧭 **Menu de Acessibilidade**: inclui botão fixo em todas as páginas para acesso rápido às ferramentas assistivas.
⚙️ **Arquitetura Modular**: pode ser facilmente integrado a qualquer sistema Django, com possibilidade de expandir para outras deficiências no futuro.

## 🚀 Tecnologias utilizadas

🐍 ** Python Python 3.13.2 **
🌐 **Django 5.1.7 **
🧠 **Vosk** – reconhecimento de voz offline
🔊 **pyttsx3** – leitura de texto (text-to-speech)
🧱 **HTML, CSS, JS (Vanilla ou com Tailwind para responsividade)**
🔁 (Opcional) Integração futura com **HandTalk API** ou outros recursos online

## 📱 Compatibilidade

O plugin foi projetado para funcionar:
✅ Em **laptops** e **computadores de secretária**
✅ Em **telemóveis** e **tablets**
✅ Mesmo **sem internet ou com internet lenta**
✅ Em qualquer sistema académico feito com **Django**

## 👩🏽‍💻 Autora
 Desenvolvido por **Gédia Jangamo**, estudante de Engenharia de Tecnologias e Sistemas de Informação, com foco em **inclusão digital e tecnologias assistivas** para
 a educação superior em Moçambique.

## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e expandir este plugin.

**Nota:** O plugin não interfere diretamente nas funcionalidades do sistema. Ele atua como uma camada de acessibilidade que melhora a experiência do utilizador.
