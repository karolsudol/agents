-- seed.sql
CREATE EXTENSION IF NOT EXISTS google_ml_integration;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS jobs (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  company VARCHAR NOT NULL,
  role VARCHAR NOT NULL,
  tech_stack VARCHAR NOT NULL,
  salary_range VARCHAR NOT NULL,
  location VARCHAR NOT NULL,
  openings INTEGER NOT NULL,
  description TEXT NOT NULL,
  description_embedding vector(3072)
);

INSERT INTO jobs (title, company, role, tech_stack, salary_range, location, openings, description) VALUES
  ('Senior Backend Engineer', 'Stripe', 'Backend', 'Go, PostgreSQL, gRPC, Kubernetes', '$180-250K/year', 'San Francisco, Hybrid', 3,
  'Design and build high-throughput microservices powering payment infrastructure for millions of businesses. Optimize Go services for sub-100ms latency at scale, work with PostgreSQL and Redis for data persistence, and deploy on Kubernetes clusters handling billions of API calls.'),
  ('Machine Learning Engineer', 'Spotify', 'Data/AI', 'Python, TensorFlow, BigQuery, Vertex AI', '$170-230K/year', 'Stockholm, Remote', 2,
  'Build and deploy ML models for music recommendation and personalization systems serving hundreds of millions of listeners. Design feature pipelines in BigQuery, train models using distributed computing, and serve predictions through real-time APIs processing thousands of requests per second.'),
  ('Frontend Engineer', 'Vercel', 'Frontend', 'React, TypeScript, Next.js', '$140-190K/year', 'Remote', 4,
  'Build developer-facing dashboard interfaces and deployment tools used by millions of developers worldwide. Create responsive, accessible React components for project management, analytics, and real-time deployment monitoring with a focus on developer experience.'),
  ('DevOps Engineer', 'Datadog', 'DevOps', 'Terraform, GCP, Docker, Kubernetes, ArgoCD', '$160-220K/year', 'New York, Hybrid', 2,
  'Manage cloud infrastructure powering an observability platform used by thousands of engineering teams. Automate deployment pipelines with ArgoCD, manage multi-cloud Kubernetes clusters, and implement infrastructure-as-code with Terraform across production environments.'),
  ('Mobile Engineer (Android)', 'Grab', 'Mobile', 'Kotlin, Jetpack Compose, GraphQL', '$120-170K/year', 'Singapore, Hybrid', 3,
  'Develop features for a super-app serving millions of users across Southeast Asia. Build modern Android UIs with Jetpack Compose, integrate GraphQL APIs, and optimize app performance for diverse device capabilities and network conditions.'),
  ('Data Engineer', 'Airbnb', 'Data', 'Python, Apache Spark, Airflow, BigQuery', '$160-210K/year', 'San Francisco, Hybrid', 2,
  'Build data pipelines that process booking, search, and pricing data for a global travel marketplace. Design ETL workflows with Apache Spark and Airflow, maintain data warehouses in BigQuery, and ensure data quality for analytics and machine learning teams.'),
  ('Full Stack Engineer', 'Revolut', 'Full Stack', 'TypeScript, Node.js, React, PostgreSQL', '$130-180K/year', 'London, Remote', 5,
  'Build the next generation of financial products making banking accessible to millions of users across 35 countries. Develop real-time trading interfaces with React and WebSockets, build Node.js APIs handling market data streams, and design PostgreSQL schemas for financial transactions.'),
  ('Site Reliability Engineer', 'Cloudflare', 'SRE', 'Go, Prometheus, Grafana, GCP, Terraform', '$170-230K/year', 'Austin, Hybrid', 2,
  'Ensure 99.99% uptime for a global network handling millions of requests per second. Define SLOs, build monitoring dashboards with Prometheus and Grafana, manage incident response, and automate infrastructure scaling across 300+ data centers worldwide.'),
  ('Cloud Architect', 'Google Cloud', 'Cloud', 'GCP, Terraform, Kubernetes, Python', '$200-280K/year', 'Seattle, Hybrid', 1,
  'Help enterprises modernize their infrastructure on Google Cloud. Design multi-region architectures, lead migration projects from on-premises to GKE, and build reference implementations using Terraform and Cloud Foundation Toolkit.'),
  ('Backend Engineer (Payments)', 'Square', 'Backend', 'Java, Spring Boot, PostgreSQL, Kafka', '$160-220K/year', 'San Francisco, Hybrid', 3,
  'Build payment processing systems handling millions of transactions for businesses of all sizes. Design event-driven architectures using Kafka, implement idempotent payment flows with Spring Boot, and ensure PCI-DSS compliance across all services.'),
  ('AI Engineer', 'Hugging Face', 'Data/AI', 'Python, LangChain, Vertex AI, FastAPI, PostgreSQL', '$150-210K/year', 'Paris, Remote', 2,
  'Build AI-powered tools for the largest open-source ML community. Develop RAG pipelines that index and search model documentation, create conversational agents using LangChain, and deploy AI services with FastAPI on cloud infrastructure.'),
  ('Platform Engineer', 'Coinbase', 'Platform', 'Rust, Kubernetes, AWS, Terraform', '$180-250K/year', 'Remote', 0,
  'Build the infrastructure platform for a leading cryptocurrency exchange. Develop high-performance matching engines in Rust, manage Kubernetes clusters for microservices, and design CI/CD pipelines that enable rapid feature deployment with zero downtime.'),
  ('QA Automation Engineer', 'Shopify', 'QA', 'Python, Selenium, Cypress, Jenkins', '$110-160K/year', 'Toronto, Hybrid', 3,
  'Design and maintain automated test suites for a commerce platform powering millions of merchants. Build end-to-end test frameworks with Cypress and Selenium, integrate tests into Jenkins CI pipelines, and establish quality gates that prevent regressions in checkout and payment flows.'),
  ('Security Engineer', 'CrowdStrike', 'Security', 'Python, SIEM, Kubernetes, Penetration Testing', '$170-240K/year', 'Austin, On-site', 1,
  'Protect enterprise customers from cyber threats on a leading endpoint security platform. Conduct penetration testing, design security monitoring with SIEM tools, implement zero-trust networking in Kubernetes environments, and lead incident response for security events.'),
  ('Product Engineer', 'GitLab', 'Full Stack', 'Go, React, PostgreSQL, Redis, GCP', '$140-200K/year', 'Remote', 4,
  'Own features end-to-end for an all-in-one DevSecOps platform used by millions of developers. Build Go microservices for CI/CD pipelines, create React frontends for code review and project management, and collaborate with product managers to iterate on user-facing features using data-driven development.');

-- Generate initial embeddings (Temporarily disabled due to Vertex AI connection issues in SQL)
-- UPDATE jobs SET description_embedding = embedding('text-embedding-004', description)::vector;
