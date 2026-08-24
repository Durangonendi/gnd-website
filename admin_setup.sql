-- GND Machinery — Admin panel + Pazar fotoğraf/kategori güncellemesi
-- Supabase Dashboard > SQL Editor > New query içine yapıştırıp "Run" a bas.
-- Bu script'i birden fazla kez çalıştırman güvenlidir (tekrar çalıştırınca hata vermez).

-- 1) Admin yetkisi
drop policy if exists "admin_select_market_requests" on market_requests;
create policy "admin_select_market_requests"
on market_requests for select
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');

drop policy if exists "admin_update_market_requests" on market_requests;
create policy "admin_update_market_requests"
on market_requests for update
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');

drop policy if exists "admin_select_quote_requests" on website_quote_requests;
create policy "admin_select_quote_requests"
on website_quote_requests for select
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');

-- 2) Pazar ilanlarına kategori ve çoklu fotoğraf desteği
alter table market_requests add column if not exists kategori text;
alter table market_requests add column if not exists foto_urls text[];

-- 3) Fotoğraf yükleme için depolama alanı (bucket)
insert into storage.buckets (id, name, public)
values ('market-photos', 'market-photos', true)
on conflict (id) do nothing;

drop policy if exists "public_read_market_photos" on storage.objects;
create policy "public_read_market_photos"
on storage.objects for select
to public
using (bucket_id = 'market-photos');

drop policy if exists "authenticated_upload_market_photos" on storage.objects;
create policy "authenticated_upload_market_photos"
on storage.objects for insert
to authenticated
with check (bucket_id = 'market-photos');
