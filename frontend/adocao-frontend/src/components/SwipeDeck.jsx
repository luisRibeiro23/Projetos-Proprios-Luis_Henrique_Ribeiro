import { useEffect, useMemo, useRef, useState } from "react";

export default function SwipeDeck({ animals, onReact, onOpen }) {
  // hooks sempre no topo
  const list = Array.isArray(animals) ? animals : [];
  const [idx, setIdx] = useState(0);
  const [anim, setAnim] = useState(null);

  const [bursts, setBursts] = useState([]);
  const idRef = useRef(1);

  // mantém idx válido se lista mudar
  useEffect(() => {
    const len = list.length;
    if (len === 0) setIdx(0);
    else setIdx((v) => (v >= len ? 0 : v));
  }, [list.length]);

  const current = list.length ? list[idx] : null;

  const likeCount = useMemo(() => {
    if (!current) return 0;
    return typeof current.like_count === "number" ? current.like_count : 0;
  }, [current]);

  const likedByMe = useMemo(() => {
    if (!current) return false;
    return !!current.liked_by_me;
  }, [current]);

  function spawnBurst(type) {
    const id = idRef.current++;
    const count = type === "STAR" ? 18 : 22;

    const items = Array.from({ length: count }).map((_, i) => ({
      key: `${id}-${i}`,
      type,
      x: 50 + (Math.random() * 18 - 9),
      y: 72 + (Math.random() * 10 - 5),
      dx: (Math.random() * 2 - 1) * 160,
      dy: -120 - Math.random() * 170,
      rot: (Math.random() * 2 - 1) * 70,
      delay: Math.random() * 0.08,
      scale: 0.8 + Math.random() * 0.9,
    }));

    setBursts((prev) => [...prev, { id, items }]);
    setTimeout(() => setBursts((prev) => prev.filter((b) => b.id !== id)), 900);
  }

  function next() {
    setIdx((v) => {
      const len = list.length;
      if (len === 0) return 0;
      return (v + 1) % len;
    });
  }

  function playAndNext(direction) {
    setAnim(direction);
    setTimeout(() => {
      next();
      setAnim(null);
    }, 220);
  }

  async function react(kind) {
    if (!current) return;

    if (kind === "LIKE") spawnBurst("HEART");
    if (kind === "SUPERLIKE") spawnBurst("STAR");

    // chama backend e ele devolve contagem + liked_by_me atualizados
    const updated = await onReact?.(current, kind);

    // ⭐: abre perfil depois de reagir (como você pediu)
    if (kind === "SUPERLIKE") {
      onOpen?.(updated || current);
      playAndNext("up");
      return;
    }

    // LIKE/DISLIKE: só vai pro próximo
    playAndNext(kind === "DISLIKE" ? "left" : "right");
  }

  // só agora pode retornar cedo
  if (!current) {
    return <p className="muted">Nenhum animal disponível por enquanto 🐾</p>;
  }

  const cover = current.__cover || current.cover || current.image_url || null;

  return (
    <div className="tinder-stage">
      <div className="burst-layer" aria-hidden="true">
        {bursts.flatMap((b) =>
          b.items.map((p) => (
            <span
              key={p.key}
              className={`burst ${p.type === "HEART" ? "burst-heart" : "burst-star"}`}
              style={{
                left: `${p.x}%`,
                top: `${p.y}%`,
                "--dx": `${p.dx}px`,
                "--dy": `${p.dy}px`,
                "--rot": `${p.rot}deg`,
                "--delay": `${p.delay}s`,
                "--scale": p.scale,
              }}
            >
              {p.type === "HEART" ? "❤️" : "⭐"}
            </span>
          ))
        )}
      </div>

      <div className={`tinder-card ${anim ? `tinder-exit-${anim}` : ""}`} onClick={() => onOpen?.(current)}>
        <div className="tinder-media">
          {cover ? <img src={cover} alt={current.name} /> : <div className="tinder-media-fallback">🐾</div>}

          <div className="tinder-badges">
            <span className="pill">{current.size}</span>
            {current.age ? <span className="pill">{current.age}</span> : null}

            <span className="pill pill-right">
              ❤️ {likeCount} {likedByMe ? "• você curtiu" : ""}
            </span>
          </div>
        </div>

        <div className="tinder-info">
          <div className="tinder-title">
            <span className="tinder-name">{current.name}</span>
          </div>
          <div className="tinder-sub">
            {current.species} • {current.city}/{current.state}
          </div>
          {current.description ? <div className="tinder-about">{current.description}</div> : null}
        </div>
      </div>

      <div className="tinder-actions">
        <button className="tinder-btn nope" onClick={() => react("DISLIKE")}>✖</button>
        <button className="tinder-btn star" onClick={() => react("SUPERLIKE")}>⭐</button>
        <button className="tinder-btn like" onClick={() => react("LIKE")}>❤️</button>
      </div>
    </div>
  );
}
