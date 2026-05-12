import logging
import os
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)

_LOGO_PATH = os.path.join(os.path.dirname(__file__), 'logo.png')


def send_credentials_email(name: str, email: str, login_email: str, password: str, role: str = 'employee'):
    """
    Send a welcome email to a newly created user with their login credentials.
    Fails silently — user creation is not rolled back if email fails.
    """
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    login_url = f"{frontend_url}/dashboard/login"
    role_label = role.capitalize()

    subject = "Welcome to Auctus — Your Account Credentials"

    text_body = f"""
Hey {name}, welcome aboard!

We're thrilled to have you with us! Your {role_label} account on Auctus is all set and ready to go.

Here are your login credentials:

  Login Email : {login_email}
  Password    : {password}

Sign in here: {login_url}

For your security, please change your password the first time you log in.

— The Auctus Team
    """.strip()

    html_body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Welcome to Auctus</title>
</head>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:'Segoe UI',Arial,sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f3f4f6;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="580" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

          <!-- Logo Header -->
          <tr>
            <td style="background:#ffffff;padding:28px 40px 22px;text-align:center;border-bottom:3px solid #00838f;">
              <img src="cid:auctus_logo" alt="Auctus" width="141" height="40"
                   style="display:block;margin:0 auto;max-width:141px;" />
            </td>
          </tr>

          <!-- Teal Banner -->
          <tr>
            <td style="background:linear-gradient(135deg,#00838f 0%,#005f6b 100%);padding:18px 40px;text-align:center;">
              <p style="margin:0;font-size:13px;color:rgba(255,255,255,0.9);letter-spacing:0.8px;text-transform:uppercase;">
                Business Management Platform
              </p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:40px 40px 32px;">
              <p style="margin:0 0 6px;font-size:24px;font-weight:800;color:#111827;">
                Hey {name}, welcome aboard! &#127881;
              </p>
              <p style="margin:0 0 6px;font-size:15px;color:#00838f;font-weight:600;">
                We're thrilled to have you with us!
              </p>
              <p style="margin:0 0 24px;font-size:15px;color:#6b7280;line-height:1.7;">
                Your <strong style="color:#111827;">{role_label}</strong> account on Auctus is all set and ready to go.
                Everything you need is just one sign-in away — let's get started! &#128640;
              </p>

              <!-- Credentials Box -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#f0faf9;border:1.5px solid #b2dfdb;border-radius:12px;margin-bottom:28px;">
                <tr>
                  <td style="padding:24px 28px;">
                    <p style="margin:0 0 4px;font-size:11px;font-weight:700;color:#00838f;letter-spacing:1px;text-transform:uppercase;">
                      Your Login Credentials
                    </p>
                    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px;">
                      <tr>
                        <td style="padding:8px 0;border-bottom:1px solid #e5e7eb;">
                          <span style="font-size:13px;color:#6b7280;font-weight:600;">Login Email</span>
                        </td>
                        <td style="padding:8px 0;border-bottom:1px solid #e5e7eb;text-align:right;">
                          <span style="font-size:14px;color:#111827;font-weight:700;">{login_email}</span>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:10px 0 0;">
                          <span style="font-size:13px;color:#6b7280;font-weight:600;">Password</span>
                        </td>
                        <td style="padding:10px 0 0;text-align:right;">
                          <span style="font-size:15px;color:#111827;font-weight:800;font-family:monospace;
                                       background:#e0f2f1;padding:4px 10px;border-radius:6px;letter-spacing:1px;">
                            {password}
                          </span>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <!-- Login Button -->
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                <tr>
                  <td align="center">
                    <a href="{login_url}"
                       style="display:inline-block;background:#00838f;color:#ffffff;text-decoration:none;
                              font-size:15px;font-weight:700;padding:14px 40px;border-radius:10px;
                              letter-spacing:0.3px;">
                      Sign In to Auctus &#8594;
                    </a>
                  </td>
                </tr>
              </table>

              <!-- Security Note -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#fffbeb;border:1.5px solid #fde68a;border-radius:10px;">
                <tr>
                  <td style="padding:14px 18px;">
                    <p style="margin:0;font-size:13px;color:#92400e;line-height:1.5;">
                      &#128274; <strong>Quick tip:</strong> For your security, please change your password the first time you log in.
                      Keep your credentials private and never share them with anyone.
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f9fafb;border-top:1px solid #f3f4f6;padding:20px 40px;text-align:center;">
              <p style="margin:0;font-size:12px;color:#9ca3af;line-height:1.6;">
                This email was sent by Auctus. If you did not expect this, please contact your administrator.<br/>
                &copy; 2026 Auctus. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>
    """.strip()

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html_body, "text/html")

        if os.path.exists(_LOGO_PATH):
            with open(_LOGO_PATH, 'rb') as f:
                logo = MIMEImage(f.read())
                logo.add_header('Content-ID', '<auctus_logo>')
                logo.add_header('Content-Disposition', 'inline', filename='logo.png')
                msg.attach(logo)

        msg.send(fail_silently=False)
        logger.info(f"Credentials email sent to {email}")
    except Exception as exc:
        print(f"[EMAIL ERROR] Failed to send to {email}: {exc}")
        logger.error(f"Failed to send credentials email to {email}: {exc}")
