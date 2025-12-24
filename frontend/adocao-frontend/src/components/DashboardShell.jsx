export default function DashboardShell({
  title,
  subtitle,
  actions,
  children,
}) {
  return (
    <div className="container">
      <div className="header">
        <div>
          <h1 className="pageTitle">{title}</h1>
          {subtitle ? <p className="pageSub">{subtitle}</p> : null}
        </div>

        {actions ? <div className="actions">{actions}</div> : null}
      </div>

      <hr />

      {children}
    </div>
  );
}
