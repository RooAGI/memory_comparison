import { cp, mkdir } from 'node:fs/promises';
await mkdir('dist/data',{recursive:true});
await mkdir('dist/results',{recursive:true});
for (const file of ['project-assessments.json','system-articles.json','a-memory.json','aeris.json','agent-memory-distillation.json','agent-memory-doctrine.json','agent-memory-engine.json','agent-memory-supabase.json','memory-systems.json']) await cp('data/'+file,'dist/data/'+file);
await cp('results/index.json','dist/results/index.json');
await cp('results/initial-baselines-status.json','dist/results/initial-baselines-status.json');
for (const file of ['REVIEW.md','METRICS.md']) await cp(file,'dist/'+file);
await cp('fixtures','dist/fixtures',{recursive:true});
await cp('articles','dist/articles',{recursive:true});
