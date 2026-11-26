import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import assessmentData from '../data/project-assessments.json';
import systemArticles from '../data/system-articles.json';
import reviewIndex from '../data/system-review-index.json';
import aMemory from '../data/a-memory.json';
import aeris from '../data/aeris.json';
import distillation from '../data/agent-memory-distillation.json';
import doctrine from '../data/agent-memory-doctrine.json';
import engine from '../data/agent-memory-engine.json';
import supabase from '../data/agent-memory-supabase.json';
import reviewMethodMarkdown from '../REVIEW.md?raw';
import './style.css';

const originalArticles = [...systemArticles.articles, aMemory.article, aeris.article, distillation.article, doctrine.article, engine.article, supabase.article];
const reviewFiles = import.meta.glob('../data/system-reviews/*.json', { import: 'default' });
const reviewedCatalog = reviewIndex.articles;
const slug = (article) => article.slug || article.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const reviewedSlugs = new Set(reviewedCatalog.map(slug));
const articles = [...originalArticles.filter((item) => !reviewedSlugs.has(slug(item))), ...reviewedCatalog];
const route = (article) => '#/article/' + encodeURIComponent(slug(article));
const status = (value) => ({ reviewed_from_code: 'Reviewed from code', not_reviewed: 'Not reviewed', not_run: 'Benchmark not run', measured: 'Measured' }[value] || value || 'Unknown');
const isExternalWebLink = (href) => typeof href === 'string' && (href.slice(0, 7).toLowerCase() === 'http://' || href.slice(0, 8).toLowerCase() === 'https://');
const externalLinkProps = (href) => isExternalWebLink(href) ? { target: '_blank', rel: 'noopener noreferrer' } : {};
const NewTabNotice = () => <span className="sr-only"> (opens in a new tab)</span>;
const results = import.meta.glob('../results/*.json', { eager: true, import: 'default' });
const manifest = results['../results/index.json'];
const records = (manifest?.records || []).map((entry) => ({ entry, data: results['../' + entry.path] }));

function App() {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const [routeHash, setRouteHash] = useState(location.hash);
  useEffect(() => { const update = () => setRouteHash(location.hash); window.addEventListener('hashchange', update); return () => window.removeEventListener('hashchange', update); }, []);
  const articleSlug = decodeURIComponent(routeHash.match(/^#\/article\/(.*)$/)?.[1] || '');
  const summaryArticle = originalArticles.find((item) => slug(item) === articleSlug && !reviewedSlugs.has(slug(item)));
  const indexedReview = reviewedCatalog.find((item) => item.slug === articleSlug);
  const [loadedReview, setLoadedReview] = useState(null);
  useEffect(() => {
    if (!indexedReview) { setLoadedReview(null); return; }
    let current = true;
    setLoadedReview(null);
    reviewFiles['../data/system-reviews/' + indexedReview.slug + '.json']?.().then((record) => {
      if (current) setLoadedReview({ ...record.article, ordinal: indexedReview.ordinal });
    });
    return () => { current = false; };
  }, [indexedReview?.slug]);
  const article = summaryArticle || (loadedReview?.slug === articleSlug ? loadedReview : null);
  const assessment = routeHash === '#/catalog';
  const isReviewMethod = routeHash === '#/method';
  const visible = useMemo(() => articles.filter((item) => {
    const terms = [item.name, item.summary, item.repository].join(' ').toLowerCase();
    return terms.includes(query.trim().toLowerCase()) && (filter === 'all' || item.source_status === filter);
  }), [query, filter]);
  return <div className="site">
    <header className="topbar"><a className="wordmark" href="#/"><img className="brand-logo" src="./favicon.png" alt="RooAGI"/> Memory systems, examined</a><nav aria-label="Main navigation"><a href="#/">System reviews</a><a href="#/catalog">Project assessment</a><a href="#/method" aria-current={isReviewMethod ? 'page' : undefined}>Review method</a><a href="mailto:lw@rooagi.com">Contact us</a></nav></header>
    {article ? <Article article={article}/> : isReviewMethod ? <ReviewMethod/> : indexedReview ? <main className="article-page" role="status">Loading review…</main> : assessment ? <Assessment/> : <main>
      <section className="intro"><div><p className="kicker">A source-led field guide</p><h1>How memory systems<br/><em>keep what matters.</em></h1><p className="lead">Agent memory tools promise to help AI systems retain and use information over time, but feature lists alone don’t show how well they work. We review code and shared workloads so teams can compare evidence, limitations, and measured results. We keep this work current by revisiting reviews as systems and evidence change.</p><a className="text-link" href="#articles">Browse the system reviews <span aria-hidden="true">↓</span></a></div><aside className="intro-note"><span className="note-index">Evidence rule</span><p>Source review and workload measurement answer different questions. They stay separate here.</p><div className="note-states"><span>Code reviewed</span><span>Benchmarks not run</span></div></aside></section>
      <section className="article-section" id="articles"><div className="section-heading"><div><p className="kicker">The review library</p><h2>Systems in focus</h2></div><p>{articles.length} detailed reviews, each tied to a repository revision and source evidence.</p></div>
        <div className="filters"><label className="search-field"><span aria-hidden="true">⌕</span><span className="sr-only">Search system reviews</span><input type="search" value={query} onChange={(e)=>setQuery(e.target.value)} placeholder="Search systems, repositories, sources"/></label><label className="filter-field">Review status<select value={filter} onChange={(e)=>setFilter(e.target.value)}><option value="all">All reviews</option><option value="reviewed_from_code">Reviewed from code</option><option value="not_reviewed">Not reviewed</option></select></label><button className="reset-filters" type="button" onClick={()=>{setQuery('');setFilter('all');}}>Reset filters</button><p className="result-count" aria-live="polite">{visible.length} of {articles.length} reviews</p></div>
        <div className="article-list">{visible.map((item,index)=><article className="article-row" key={slug(item)}><span className="row-number">{String(item.ordinal || index+1).padStart(2,'0')}</span><div className="row-main"><h3><a href={route(item)}>{item.name}</a></h3><p>{item.summary}</p><div className="row-meta"><a href={item.repository} {...externalLinkProps(item.repository)}>{item.repository.replace(/^https?:\/\//,'')}{isExternalWebLink(item.repository)&&<NewTabNotice/>}</a><span>{item.branch} · {item.revision.slice(0,8)}</span></div></div><div className="row-status"><span className="status-chip reviewed">{status(item.source_status || 'reviewed_from_code')}</span><span className="status-chip pending">{status(item.benchmark_status)}</span><a className="read-link" href={route(item)}>Read review <span aria-hidden="true">↗</span></a></div></article>)}{visible.length===0&&<p className="empty">No reviews match. Try another name or clear the status filter.</p>}</div>
      </section>
      <section className="evidence-strip"><div><span className="status-chip reviewed">Reviewed from code</span><p>Findings are scoped to the pinned upstream revision and linked sources.</p></div><div><span className="status-chip pending">Benchmark not run</span><p>No workload observations are implied by source review.</p></div><a href="#/catalog">See project assessment records <span aria-hidden="true">↗</span></a></section>
    </main>}
    <footer className="footer"><span>Memory systems comparison</span><span>Project criteria · source evidence · measured results</span><span><strong>Each system review is conducted end-to-end by a RooAGI agent on the RooAGI Agents Platform.</strong> RooAGI develops Membrick. Contact: <a href="mailto:lw@rooagi.com">lw@rooagi.com</a></span><a href="METRICS.md">Metric definitions</a></footer>
  </div>;
}

function inlineMarkdown(text) {
  return text.split(/(\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*|`[^`]+`)/g).filter(Boolean).map((part, index) => {
    const link = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if (link) return <a key={index} href={link[2]} {...externalLinkProps(link[2])}>{link[1]}{isExternalWebLink(link[2])&&<NewTabNotice/>}</a>;
    if (part.startsWith('**') && part.endsWith('**')) return <strong key={index}>{part.slice(2, -2)}</strong>;
    if (part.startsWith('`') && part.endsWith('`')) return <code key={index}>{part.slice(1, -1)}</code>;
    return part;
  });
}

function methodBlocks(markdown) {
  const lines = markdown.split(/\r?\n/);
  const blocks = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i].trim();
    if (!line) { i += 1; continue; }
    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      if (heading[1].length > 1) {
        const level = Math.min(3, heading[1].length);
        const Tag = `h${level}`;
        blocks.push(<Tag key={`heading-${i}`}>{inlineMarkdown(heading[2])}</Tag>);
      }
      i += 1;
      continue;
    }
    const list = line.match(/^(?:[-*]\s+|\d+\.\s+)/);
    if (list) {
      const ordered = /^\d+\.\s+/.test(line);
      const items = [];
      while (i < lines.length && (lines[i].trim().match(/^(?:[-*]\s+|\d+\.\s+)/))) {
        items.push(<li key={`item-${i}`}>{inlineMarkdown(lines[i].trim().replace(/^(?:[-*]\s+|\d+\.\s+)/, ''))}</li>);
        i += 1;
      }
      const Tag = ordered ? 'ol' : 'ul';
      blocks.push(<Tag key={`list-${i}`}>{items}</Tag>);
      continue;
    }
    const paragraph = [line];
    i += 1;
    while (i < lines.length && lines[i].trim() && !/^(#{1,6})\s+/.test(lines[i].trim()) && !/^(?:[-*]\s+|\d+\.\s+)/.test(lines[i].trim())) {
      paragraph.push(lines[i].trim());
      i += 1;
    }
    blocks.push(<p key={`paragraph-${i}`}>{inlineMarkdown(paragraph.join(' '))}</p>);
  }
  return blocks;
}

function ReviewMethod() {
  return <main className="method-page"><nav className="breadcrumbs" aria-label="Breadcrumb"><a href="#/">System reviews</a><span aria-hidden="true">/</span><span>Review method</span></nav><header className="method-head"><p className="kicker">Project-owned method</p><h1>Review method</h1><p className="lead">How source evidence, project assessments, benchmark measurements, and remaining unknowns are recorded.</p><p className="method-credit">Each system review is conducted end-to-end by a RooAGI agent using the RooAGI Agents Platform. The <a href="https://neoneye.github.io/agent-memory-atlas/" {...externalLinkProps('https://neoneye.github.io/agent-memory-atlas/')}>Agent Memory Atlas<NewTabNotice/></a> inspired this project and helped us discover systems to study. RooAGI develops Membrick.</p></header><article className="method-content">{methodBlocks(reviewMethodMarkdown)}</article><nav className="article-bottom"><a href="#/">← Return to all systems</a><a href="#/catalog">Project assessment →</a></nav></main>;
}

function Article({article:a}) {
  const sources=a.sources||[], repo=a.repository||'', revision=a.revision||'', revUrl=repo.replace(/\/$/,'')+'/commit/'+revision;
  const benchmarkRows=a.benchmark?.length?a.benchmark:[{text:a.benchmark_note||'Benchmark status not_run; no source-grounded workload result is available.',sources:[]}];
  const groups=[['who','Identity and scope',a.who_what||[]],['architecture','Architecture and data model',a.architecture||[]],['behavior','Operations and retrieval',a.behavior||[]],['limits','Limits and unknowns',a.limits||[]],['benchmark','Benchmark status',benchmarkRows]];
  const evidence=(ids=[])=>ids.map((id,i)=>{const source=sources.find((x)=>x.id===id);const href=source?.url?.startsWith('./')?source.url.slice(2):source?.url;return <React.Fragment key={id}>{i?'; ':''}{source?<a href={href} {...externalLinkProps(href)}>{source.label}{isExternalWebLink(href)&&<NewTabNotice/>}</a>:id}</React.Fragment>});
  return <main className="article-page"><nav className="breadcrumbs" aria-label="Breadcrumb"><a href="#/">All system reviews</a><span aria-hidden="true">/</span><span>{a.name}</span></nav>
    <header className="article-head"><p className="kicker">Project source review · pinned upstream revision</p><h1>{a.name}</h1><p className="lead">{a.summary}</p><div className="status-line"><span className="status-chip reviewed">{status(a.source_status)}</span><span className="status-chip pending">{status(a.benchmark_status)}</span></div><p className="article-meta">Repository <a href={repo} {...externalLinkProps(repo)}>{repo}{isExternalWebLink(repo)&&<NewTabNotice/>}</a><br/>Default branch {a.branch} · reviewed {a.reviewed_at} {a.review_timezone||''}<br/>Commit <a href={revUrl} {...externalLinkProps(revUrl)}><code>{revision}</code><NewTabNotice/></a></p></header>
    <p className="article-callout"><strong>Source inspection is not benchmark measurement.</strong> This review records implementation evidence at one revision. Benchmark values remain unavailable until a versioned workload result is recorded and adjudicated.</p>
    <nav className="section-nav" aria-label="Page sections">{[...groups.map(([id,title])=>[id,title]),['metrics','Metric evidence'],['sources','Sources']].map(([id,title])=><a key={id} href={'#section-'+id} onClick={(event)=>{event.preventDefault();document.getElementById('section-'+id)?.scrollIntoView({behavior:'smooth'});}}>{title}</a>)}</nav>
    {groups.slice(0,3).map(([id,title,rows])=><ArticleSection key={id} id={id} title={title} rows={rows} evidence={evidence}/>)}
    <section className="article-panel" id="section-metrics"><p className="kicker">Evidence by domain</p><h2>Metric-domain evidence</h2><p className="section-intro">Code observations describe available mechanisms. Only captured and adjudicated workload records can establish measured outcomes.</p>{(a.metrics||[]).map((m)=><div className="metric-row" key={m.domain}><div><h3>{m.domain}</h3><span className="status-chip neutral">{m.status}</span></div><div><p>{m.evidence}</p><p className="evidence-links">Evidence: {evidence(m.sources)}</p></div></div>)}</section>
    {groups.slice(3).map(([id,title,rows])=><ArticleSection key={id} id={id} title={title} rows={rows} evidence={evidence}/>)}
    <section className="article-panel" id="section-sources"><p className="kicker">Trace the review</p><h2>Sources and provenance</h2><ul className="source-list">{sources.map((s)=><li key={s.id}><a href={s.url} {...externalLinkProps(s.url)}>{s.label}{isExternalWebLink(s.url)&&<NewTabNotice/>}</a><span>{s.path||'Project source'}{s.symbol?' · '+s.symbol:''}</span></li>)}</ul><p className="provenance">Reviewed at <a href={revUrl} {...externalLinkProps(revUrl)}>{revision}<NewTabNotice/></a>. {a.atlas_locator&&<>Repository locator attribution: Agent Memory Atlas, pin {a.atlas_locator.revision}; <a href={a.atlas_locator.url} {...externalLinkProps(a.atlas_locator.url)}>source locator{isExternalWebLink(a.atlas_locator.url)&&<NewTabNotice/>}</a>.</>}</p></section><nav className="article-bottom"><a href="#/">← Return to all systems</a><a href="#section-who" onClick={(event)=>{event.preventDefault();document.getElementById('section-who')?.scrollIntoView({behavior:'smooth'});}}>Back to top ↑</a></nav>
  </main>;
}
function ArticleSection({id,title,rows,evidence}) { return <section className="article-panel" id={'section-'+id}><p className="kicker">Source findings</p><h2>{title}</h2>{rows.map((row,i)=><div className="finding" key={i}><p>{row.text}</p><p className="evidence-links">Evidence: {evidence(row.sources||[])}</p></div>)}</section>; }

function Assessment() {
 return <main className="assessment-page"><p className="kicker">Project-owned criteria</p><h1>Project assessment</h1><p className="lead">Project criteria and benchmark records are distinct from detailed system reviews and discovery references.</p><div className="criteria-list">{assessmentData.criteria.map((c)=><article key={c.id}><h2>{c.label}</h2><p>{c.definition}</p><span>{c.evidence_mode} evidence</span></article>)}</div><section className="results-list"><p className="kicker">Versioned workload records</p><h2>Benchmark records and provenance</h2><p>Execution status, adjudication, and measurement remain distinct. Planned fixture counts are not observed denominators.</p>{records.map(({entry,data})=><article key={entry.path}><h3>Execution status · {entry.label||entry.path}</h3><p>{data?.note||'See the versioned record for status details.'}</p><a href={entry.path}>Open raw source record</a></article>)}</section></main>;
}
createRoot(document.getElementById('root')).render(<App/>);
