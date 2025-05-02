from flask import session


def render_page(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{title}</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
        <style>
          body {{
            background: #f8f9fa;
          }}
          .navbar-brand {{
            font-weight: bold;
          }}
          .content {{
            padding: 20px 0;
          }}
        </style>
    </head>
    <body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Train Reservation System</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor"
          aria-controls="navbarColor" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarColor">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="/">Main Page</a></li>
            {f'<li class="nav-item"><a class="nav-link" href="/auth/logout">Logout</a></li>' if session.get('role') else '<li class="nav-item"><a class="nav-link" href="/auth/login_passenger">Login</a></li>'}
          </ul>
        </div>
      </div>
    </nav>

    <div class="container my-4">
      <h1 class="mb-4">{title}</h1>
      {content}
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """