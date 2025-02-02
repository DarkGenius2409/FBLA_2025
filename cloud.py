from supabase import create_client, Client

url = "https://jorpdfqkpteghuezmhky.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpvcnBkZnFrcHRlZ2h1ZXptaGt5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg1MTY2MzAsImV4cCI6MjA1NDA5MjYzMH0.BeBXopabbywgL2-oVEDgCdMr3SDCLQkQy1PV1BElOUY"

supabase: Client = create_client(url, key)