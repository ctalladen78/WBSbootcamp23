
# translate categories
-- informatica_acessorios, pcs, pc_gamer, eletronicos,relogios_presentes,consoles_games
-- select distinct p.product_category_name as esp, product_category_name_english as en
-- from products as p
-- left join product_category_name_translation as t
-- on p.product_category_name = t.product_category_name

# tech count products
-- select 
-- count(*)
-- from products
-- where product_category_name =
-- 'informatica_acessorios'#1639
-- 'pcs'#30
-- 'pc_gamer'#3
-- 'eletronicos'#517
-- 'relogios_presentes'#1329
-- 'consoles_games'#317
-- 'eletroportateis'
-- 'telefonia'
-- 'audio'
-- all products#32951

# avg overall tech revenue
-- select avg(payment_value) as techRevenue,product_category_name as cat
-- from products as p
-- left join order_items as i
-- on p.product_id = i.product_id
-- left join orders as o
-- on i.order_id = o.order_id
-- left join order_payments as py
-- on o.order_id = py.order_id 
-- where product_category_name in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )
-- group by cat


# avg overall monthly revenue
-- select avg(payment_value), extract(month from order_purchase_timestamp) as mo

# avg annual tech revenue 
-- select avg(payment_value), extract(year from order_purchase_timestamp) as yr

# average monthly tech revenue 
-- select avg(payment_value) as avgRevenue, extract(month from order_purchase_timestamp) as mo
-- from products as p
-- left join order_items as i
-- on p.product_id = i.product_id
-- left join orders as o
-- on i.order_id = o.order_id
-- left join order_payments as py
-- on o.order_id = py.order_id 
-- where product_category_name in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )
-- group by mo 
-- order by mo desc

# high value items
# avg freight cost vs month (monthly spend) overall
# avg freight cost vs month (monthly spend) tech
-- select avg(freight_value) as transport_costs, extract(month from order_purchase_timestamp) as mo
-- from products as p
-- left join order_items as i
-- on p.product_id = i.product_id
-- left join orders as o
-- on i.order_id = o.order_id
-- where product_category_name in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )
-- group by mo 
-- order by mo desc

# high value items
# avg order price per category
-- select avg(price),product_category_name as cat
-- from products as p
-- left join order_items as i
-- on p.product_id = i.product_id
-- where product_category_name in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )
-- group by cat

# avg review score per category
-- select avg(review_score),product_category_name as cat
-- from products as p
-- left join order_items as i
-- on p.product_id = i.product_id
-- left join orders as o
-- on i.order_id = o.order_id
-- left join order_reviews as r
-- on o.order_id = r.order_id
-- where product_category_name in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )
-- group by cat


# avg difference between order placed - delivered
# count tech orders delivered ontime
-- select count(*)
-- from products as p
-- left join order_items as i
-- on p.product_id = i.product_id
-- left join orders as o
-- on i.order_id = o.order_id
-- where product_category_name in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )
-- and order_status = 'delivered'

# count orders delivered delayed
# count orders exceeded delivery estimate
-- select count(o.order_id) as orders,order_estimated_delivery_date,order_delivered_customer_date,o.order_id
-- from products as p
-- left join order_items as i
-- on p.product_id = i.product_id
-- left join orders as o
-- on i.order_id = o.order_id
-- where product_category_name in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )
-- and o.order_estimated_delivery_date > o.order_delivered_customer_date
-- group by order_id


# top ten cities of customers which order tech categories
-- select count(*) as orders ,city
-- from products as p
-- left join order_items as i
-- on p.product_id = i.product_id
-- left join orders as o
-- on i.order_id = o.order_id
-- left join customers as cu
-- on cu.customer_id = o.customer_id
-- left join geo
-- on cu.customer_zip_code_prefix = geo.zip_code_prefix
-- where product_category_name in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )
-- group by city
-- order by orders desc
-- limit 10

# count tech orders
-- select
-- count(order_item_id)
-- from products
-- left join order_items
-- on products.product_id = order_items.product_id
-- where product_category_name
-- in (
-- 'informatica_acessorios',
-- 'pcs',
-- 'pc_gamer',
-- 'eletronicos',
-- 'relogios_presentes',
-- 'consoles_games',
-- 'eletroportateis',
-- 'telefonia',
-- 'audio'
-- )


