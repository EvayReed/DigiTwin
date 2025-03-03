from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Server running status"])


@router.get("/",
            summary="self-check program",
            description="When you see this message, it means that the Lord's light waves have successfully connected!",
            response_class=HTMLResponse)
async def health_check():
    return """
    <style>
    body {
        background: linear-gradient(-45deg, #0f0f1a, #1a1a2f, #2d0f39);
        background-size: 400% 400%;
        animation: gradient 15s infinite;
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #0ff;
        text-shadow: 0 0 10px #0ff;
    }

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        100% {background-position: 100% 50%;}
    }

    h1 {
        font-size: 3em;
        animation: flicker 10s alternate;
    }

    a {
        font-size: 1.5em;
        color: #f0f;
        text-decoration: none;
        border: 2px solid #f0f;
        padding: 10px 20px;
        border-radius: 5px;
        transition: all 0.3s;
        box-shadow: 0 0 15px #f0f;
    }

    a:hover {
        transform: scale(1.1);
        background: rgba(255,0,255,0.1);
    }

    @keyframes flicker {
        0%, 18%, 22%, 25%, 53%, 57%, 100% {
            text-shadow: 0 0 10px #0ff,
                         0 0 20px #0ff,
                         0 0 30px #0ff;
        }
        20%, 24%, 55% {
            text-shadow: none;
        }
    }
    </style>

    <h1>⚡️ The server is running properly.！⚡️</h1>
    <a href="http://0.0.0.0:9527/docs">🚀 View interface documentation</a>
    """