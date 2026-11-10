HEAD_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl" id="html-root">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>UES SMART ERP — المتحدة للخدمات التعليمية | Desktop & Enterprise Platform</title>
  <link href="/assets/ues.css" rel="stylesheet">

  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'">
  <style>
    :root {
      --primary-navy: #0B1F33;
      --secondary-navy: #142C46;
      --teal: #0D9488;
      --teal-hover: #0F766E;
      --bg-main: #F5F7FA;
      --white: #FFFFFF;
      --dark-text: #172033;
      --muted-text: #64748B;
      --success: #16A34A;
      --warning: #F59E0B;
      --danger: #DC2626;
      --border-col: #E2E8F0;
    }
    * { box-sizing: border-box; }
    body {
      font-family: 'Cairo', 'Inter', sans-serif;
      background-color: var(--bg-main);
      color: var(--dark-text);
      margin: 0;
      padding: 0;
      overflow-x: hidden;
    }
    html.dark body {
      background-color: #071422;
      color: #F1F5F9;
    }
    html.dark .surface-card {
      background-color: #0B1F33 !important;
      border-color: #1E3A5F !important;
      color: #F1F5F9 !important;
    }
    html.dark .surface-sub {
      background-color: #142C46 !important;
      border-color: #23456E !important;
      color: #E2E8F0 !important;
    }
    html.dark input, html.dark select, html.dark textarea {
      background-color: #142C46 !important;
      border-color: #2A4B7C !important;
      color: #F8FAFC !important;
    }
    .ltr-num {
      font-family: 'Inter', sans-serif;
      direction: ltr;
      unicode-bidi: embed;
      display: inline-block;
    }
    .desktop-titlebar {
      background: linear-gradient(90deg, #071422 0%, #0B1F33 50%, #142C46 100%);
      height: 34px;
      user-select: none;
    }
    .sidebar-scroll::-webkit-scrollbar, .custom-scroll::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .sidebar-scroll::-webkit-scrollbar-thumb, .custom-scroll::-webkit-scrollbar-thumb {
      background: rgba(100, 116, 139, 0.35);
      border-radius: 9999px;
    }
    @media print {
      .no-print { display: none !important; }
      body { background: #fff !important; color: #000 !important; }
    }
  </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-teal selection:text-white">
  <div id="app-root" class="flex-1 flex flex-col min-h-screen"></div>
  <div id="modal-container"></div>
  <div id="toast-container" class="fixed bottom-5 left-5 z-50 flex flex-col gap-2 max-w-md pointer-events-none"></div>
"""
