-- GND Machinery — Admin panel yetkilendirme
-- Bunu Supabase Dashboard > SQL Editor > New query içine yapıştırıp "Run" a bas.
-- Sadece kuralsz_drn3444@hotmail.com hesabına market_requests ve
-- website_quote_requests tablolarında tam görüntüleme/onay yetkisi verir.
-- Diğer kullanıcıların erişimini etkilemez.

create policy "admin_select_market_requests"
on market_requests for select
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');

create policy "admin_update_market_requests"
on market_requests for update
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');

create policy "admin_select_quote_requests"
on website_quote_requests for select
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');
